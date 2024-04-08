from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from .models import Account, Car, Snippet, DutiesTrouble, Checklist, Process
from .forms import SnippetForm, DutiesTroubleForm, ProcessForm, ChecklistForm
import openpyxl


# Create your views here.
def top(request):
    return HttpResponse("日報一覧画面")


def snippet_new(request):
    return HttpResponse("日報新規登録画面 1つ目の編集項目の方")


def snippet_new_checklist(request):
    return HttpResponse("日報新規登録画面 2つ目のチェックリストの方")


def snippet_update(request):
    return HttpResponse("日報編集画面 1つ目の編集項目の方")


def snippet_update_checklist(request):
    return HttpResponse("日報編集画面 2つ目のチェックリストの方")


def pre_car_registration(request):
    return HttpResponse("車両登録前画面")


def car_registration(request):
    return HttpResponse("車両登録画面")


def get_employee(request):
    return HttpResponse("社員情報画面")


class SnippetListView(View):
    def get(self, request):
        # 記録してある投稿の全データを投稿時間を元にソートして表示
        # snippets は存在する時点で提出済みとみなす
        snippets = Snippet.objects.all().order_by("-create_at")

        # bool -> True = 1. False = 0
        # 未提出 = is_snippet_make が False
        # filter(is_snippet_make=0) で is_snippet_make が 0 のデータ、
        # つまり snippets で選択されていないデータのみを取得する
        not_submitted_checklist = (
            Checklist.objects.all().order_by("-create_at").filter(is_snippet_make=0)
        )
        # トップページのhtmlへ日報データをテンプレートに渡す
        return render(
            request,
            "snippet_list.html",
            {"posts": snippets, "checklists": not_submitted_checklist},
        )

snippet_list = SnippetListView.as_view()

# snippet画面の表示/POST後処理
class SnippetView(View):
    # 新規入力画面へ
    def get(self, request, checklist_id):
        # 投稿ボタンで投稿ページへ
        return render(
            request,
            "snippet_post.html",
            {
                "form": SnippetForm,
                "form_trouble": DutiesTroubleForm,
                "form_process": ProcessForm,
                "process_count": 1,
                "checklist_id": checklist_id
            },
        )

    # 投稿機能
    def post(self, request, checklist_id):
        req = request.POST
        # 取得したchecklist_idを該当のChecklistへ変換
        checklist = Checklist.objects.get(pk=checklist_id)
        # スニペットフォーム保存
        # checklists_id挿入のための
        # モデルデータ作成
        gasoline = req.get("gasoline_amount")
        if gasoline == "":
            gasoline = 0.0
        oil = req.get("oil")
        if oil == "":
            oil = 0.0

        snippet = Snippet( 
            # 末尾の [0] について
            # 入力項目のうち同一名のデータは、
            # request.POST に配列で記録され、
            # snippet においては index[0] を使用する
            checklist_id=checklist,
            start_time=req.getlist("start_time")[0],
            end_time=req.getlist("end_time")[0],
            start_point=req.getlist("start_point")[0],
            end_point=req.getlist("end_point")[0],
            start_mileage=req.get("start_mileage"),
            end_mileage=req.get("end_mileage"),
            break_spot=req.get("break_spot"),
            weather=req.get("weather"),
            gasoline_amount=gasoline,
            oil=oil,
            driving_time=req.get("driving_time"),
            non_driving_time=req.get("non_driving_time"),
            break_time=req.get("break_time"),
            is_today_trouble=req.get("is_today_trouble"),
            free_space=req.get("free_space"),
        )
        if snippet.is_today_trouble == "on":
            snippet.is_today_trouble = True
        else:
            snippet.is_today_trouble = False
        snippet.save()

        # チェックリストフォーム保存
        checklist.is_snippet_make = True  # 提出済みへ変更
        checklist.save()

        # 業務トラブルフォーム保存
        duties_trouble = DutiesTrouble(
            snippet_id=snippet,
            trouble_situation=req.get("trouble_situation"),
            trouble_cause=req.get("trouble_cause"),
            trouble_support=req.get("trouble_support"),
        )
        duties_trouble.save()

        # 工程テーブルフォーム保存
        form_process_count = len(req.getlist("via_point"))
        for i in range(form_process_count):
            process = Process(
                snippet_id=snippet,
                start_time=req.getlist("start_time")[i + 1],
                end_time=req.getlist("end_time")[i + 1],
                start_point=req.getlist("start_point")[i + 1],
                end_point=req.getlist("end_point")[i + 1],
                via_point=req.getlist("via_point")[i],
                client=req.getlist("client")[i],
                goods=req.getlist("goods")[i],
                load_situation=req.getlist("load_situation")[i],
                load_mileage=req.getlist("load_mileage")[i],
                hollow_mileage=req.getlist("hollow_mileage")[i],
                is_load_situation=req.getlist("is_load_situation")[i],
            )
            if process.is_load_situation == "on":
                process.is_load_situation = True
            else:
                process.is_load_situation = False

            process.save()
        # トップ画面へ
        return redirect(to="snippet_list")

snippet_post = SnippetView.as_view()


# checklist入力画面表示/POST処理
class ChecklistView(View):
    # 新規入力画面
    def get(self, request):
        # 点検ページへ
        return render(
            request,
            "snippet_checklist.html",
            {
                "form": ChecklistForm,
            },
        )

    # 投稿機能
    def post(self, request):
        # チェックリストテーブルへの保存
        checklist = ChecklistForm(
            request.POST,
        )
        # 【Process form との bool 入力処理の違い】
        # チェックボックス(bool)のリクエスト値は
        # 内部的に "on" か "off" で受け取っていた。
        # Process form 側では if 文による True/False への変換を行ったが
        # form クラスの引数に request.POST を渡す場合、
        # 変換しなくてもいい感じに bool で登録してくれる
        if checklist.is_valid():
            checklist.save()

        return redirect(to="snippet_list")

checklist_post = ChecklistView.as_view()

class ChecklistEditView(View):
    def get(self, request, checklist_id):
        post = get_object_or_404(Checklist, pk=checklist_id)
        edit_form = ChecklistForm(instance=post)
        return render(
            request, 
            "checklist_edit.html",
              {'form': edit_form,'post':post}
        )
    def post(self, request, checklist_id):
        checklist = Checklist(
            request.POST,
        )
        checklist.pk = checklist_id
        post = get_object_or_404(Checklist, pk=checklist_id)
        form = ChecklistForm(request.POST, instance=post)
        form.save()
        return redirect(to="snippet_list")

checklist_edit = ChecklistEditView.as_view()

class SnippetEditView(View):
    def get(self, request, snippet_id):
        post_snippet = get_object_or_404(Snippet, pk=snippet_id)
        post_trouble = get_object_or_404(DutiesTrouble, snippet_id=snippet_id)
        post_process = get_list_or_404(Process, snippet_id=snippet_id)
        process_len = len(post_process)
        edit_SnippetForm = SnippetForm(instance=post_snippet)
        edit_TroubleForm = DutiesTroubleForm(instance=post_trouble)
        edit_ProcessForm = []
        checklist_id = post_snippet.checklist_id
        for i in range(process_len):
            edit_ProcessForm.append(ProcessForm(instance=post_process[i]))
        return render(request, "snippet_edit.html", {'form': edit_SnippetForm,'form_trouble': edit_TroubleForm,'form_process': edit_ProcessForm,'process_count': process_len,'checklist_id':checklist_id})
    def post(self, request,snippet_id):
            req = request.POST
            post_snippet = get_object_or_404(
                Snippet,
                pk=snippet_id
            )
            post_trouble = get_object_or_404(
                DutiesTrouble, 
                snippet_id=snippet_id
            )
            post_process = get_list_or_404(
                Process,
                snippet_id=snippet_id
            )
            checklist_id = post_snippet.checklist_id
            # スニペットフォーム保存
            # checklists_id挿入のための
            # モデルデータ作成
            gasoline = req.get("gasoline_amount")
            if gasoline == "":
                gasoline = 0.0
            oil = req.get("oil")
            if oil == "":
                oil = 0.0

            snippet = Snippet(
                id = post_snippet.pk,
                checklist_id=checklist_id,
                # 末尾の [0] について
                # 入力項目のうち同一名のデータは、
                # request.POST に配列で記録され、
                # snippet においては index[0] を使用する
                start_time=req.getlist("start_time")[0],
                end_time=req.getlist("end_time")[0],
                start_point=req.getlist("start_point")[0],
                end_point=req.getlist("end_point")[0],
                start_mileage=req.get("start_mileage"),
                end_mileage=req.get("end_mileage"),
                break_spot=req.get("break_spot"),
                weather=req.get("weather"),
                gasoline_amount=gasoline,
                oil=oil,
                driving_time=req.get("driving_time"),
                non_driving_time=req.get("non_driving_time"),
                break_time=req.get("break_time"),
                is_today_trouble=req.get("is_today_trouble"),
                free_space=req.get("free_space"),
                create_at=post_snippet.create_at
            )
            if snippet.is_today_trouble == "on":
                snippet.is_today_trouble = True
            else:
                snippet.is_today_trouble = False
            snippet.save()

            # 業務トラブルフォーム保存
            duties_trouble = DutiesTrouble(
                id=post_trouble.id,
                snippet_id=post_trouble.snippet_id,
                trouble_situation=req.get("trouble_situation"),
                trouble_cause=req.get("trouble_cause"),
                trouble_support=req.get("trouble_support"),
            )
            post_trouble.delete()
            duties_trouble.save()
            
            
            # 工程テーブルフォーム保存
            form_process_count = len(req.getlist("via_point"))
            for i in range(form_process_count):
                process = Process(
                    id=post_process[i].id,
                    snippet_id=post_process[i].snippet_id,
                    start_time=req.getlist("start_time")[i + 1],
                    end_time=req.getlist("end_time")[i + 1],
                    start_point=req.getlist("start_point")[i + 1],
                    end_point=req.getlist("end_point")[i + 1],
                    via_point=req.getlist("via_point")[i],
                    client=req.getlist("client")[i],
                    goods=req.getlist("goods")[i],
                    load_situation=req.getlist("load_situation")[i],
                    load_mileage=req.getlist("load_mileage")[i],
                    hollow_mileage=req.getlist("hollow_mileage")[i],
                    is_load_situation=req.getlist("is_load_situation")[i],
                )
                if process.is_load_situation == "on":
                    process.is_load_situation = True
                else:
                    process.is_load_situation = False
                post_process[i].delete()
                process.save()
            post_snippet=snippet
            # トップ画面へ
            return redirect(to="snippet_list")
snippet_edit = SnippetEditView.as_view()

def excelfile_download(request, snippet_pk):
    # Excelのテンプレートファイルの読み込み
    wb = openpyxl.load_workbook(
        "./snippets/static/excel/report.xlsx"
    )
    # 入力対象のシート指定
    sheet = wb["report_sheet"]
    # snippetテーブル
    snippet_data = get_object_or_404(Snippet, pk=snippet_pk)
    sheet["E6"] = (
        str(snippet_data.start_time.hour) 
        + ":" 
        + str(snippet_data.start_time.minute)
    )
    sheet["E8"] = (
        str(snippet_data.end_time.hour) 
        + ":" 
        + str(snippet_data.end_time.minute)
    )
    sheet["I6"] = snippet_data.start_point
    sheet["W6"] = snippet_data.end_point
    sheet["Q6"] = (
        str(snippet_data.start_time.hour) 
        + ":" 
        + str(snippet_data.start_time.minute)
    )
    sheet["AE6"] = (
        str(snippet_data.end_time.hour) 
        + ":" 
        + str(snippet_data.end_time.minute)
    )
    weekday = snippet_data.checklist_id.working_day.weekday()
    weeklist = ["月","火","水","木","金","土","日"]
    week = weeklist[weekday]
    sheet["A3"] = (
        str(snippet_data.checklist_id.working_day.year)
        + " 年  "
        + str(snippet_data.checklist_id.working_day.month)
        + " 月  "
        + str(snippet_data.checklist_id.working_day.day)
        + " 日  " 
        + "( "
        + week
        + " 曜日)  "+ "天候 "
        + "( "
        + snippet_data.weather
        + " )"
    )
    sheet["AR3"] = snippet_data.checklist_id.car_id.vehicle_number
    sheet["AO8"] = (
        snippet_data.checklist_id.account_id.last_name
        + " "
        + snippet_data.checklist_id.account_id.first_name
    )
    sheet["I9"] = snippet_data.start_mileage
    sheet["S9"] = snippet_data.end_mileage

    today_mileage = snippet_data.end_mileage - snippet_data.start_mileage
    if today_mileage >= 0:
        sheet["AB9"] = today_mileage
    if snippet_data.gasoline_amount != False:
        sheet["E36"] = snippet_data.gasoline_amount
    if snippet_data.oil != False:
        sheet["I36"] = snippet_data.oil

    sheet["BD18"] = (
        str(snippet_data.driving_time.hour)
        + ":"
        + str(snippet_data.driving_time.minute)
    )
    sheet["BD19"] = (
        str(snippet_data.non_driving_time.hour)
        + ":"
        + str(snippet_data.non_driving_time.minute)
    )
    sheet["BD20"] = (
        str(snippet_data.break_time.hour) 
        + ":" 
        + str(snippet_data.break_time.minute)
    )
    work_minute = (
        snippet_data.driving_time.minute 
        + snippet_data.non_driving_time.minute
    )

    work_hour = 0
    if work_minute >= 60:
        work_minute -= 60
        work_hour += 1
    work_hour += snippet_data.driving_time.hour 
    + snippet_data.non_driving_time.hour

    sheet["BG18"] = str(work_hour) + ":" + str(work_minute)
    breek_in_minute = work_minute 
    + snippet_data.break_time.minute
    breek_in_hour = work_hour
    if breek_in_minute >= 60:
        breek_in_minute -= 60
        breek_in_hour += 1
    breek_in_hour += snippet_data.break_time.hour
    sheet["BI18"] = str(breek_in_hour) + ":" + str(breek_in_minute)
    sheet["BF36"] = snippet_data.free_space
    sheet["H21"] = snippet_data.break_spot
    # チェックリストテーブル
    # 左列
    if snippet_data.checklist_id.is_before_trouble == True:
        sheet["AB41"] = "✔"
    if snippet_data.checklist_id.is_tire_damage == True:
        sheet["AB42"] = "✔"
    if snippet_data.checklist_id.is_tire_groove == True:
        sheet["AB43"] = "✔"
    if snippet_data.checklist_id.is_tire_parts == True:
        sheet["AB44"] = "✔"
    if snippet_data.checklist_id.is_radiator == True:
        sheet["AB45"] = "✔"
    if snippet_data.checklist_id.is_brake_oil == True:
        sheet["AB46"] = "✔"
    if snippet_data.checklist_id.is_air_tank == True:
        sheet["AB47"] = "✔"
    if snippet_data.checklist_id.is_engine_oil == True:
        sheet["AB48"] = "✔"
    if snippet_data.checklist_id.is_battery == True:
        sheet["AB49"] = "✔"
    if snippet_data.checklist_id.is_belt == True:
        sheet["AB50"] = "✔"
    if snippet_data.checklist_id.is_parking_brake == True:
        sheet["AB51"] = "✔"
    # 右列
    if snippet_data.checklist_id.is_washer_fluid == True:
        sheet["BJ41"] = "✔"
    if snippet_data.checklist_id.is_engine == True:
        sheet["BJ42"] = "✔"
    if snippet_data.checklist_id.is_air_brake == True:
        sheet["BJ43"] = "✔"
    if snippet_data.checklist_id.is_light == True:
        sheet["BJ44"] = "✔"
    if snippet_data.checklist_id.is_brake_pedal == True:
        sheet["BJ45"] = "✔"
    if snippet_data.checklist_id.is_brake_details == True:
        sheet["BJ46"] = "✔"

    # トラブルテーブル
    trouble_data = get_object_or_404(DutiesTrouble, snippet_id=snippet_pk)
    if trouble_data.trouble_situation != False:
        sheet["AC36"] = trouble_data.trouble_situation
    if trouble_data.trouble_cause != False:
        sheet["AC37"] = trouble_data.trouble_cause
    if trouble_data.trouble_support != False:
        sheet["AU36"] = trouble_data.trouble_support

    # 工程テーブル
    process_list = get_list_or_404(Process, snippet_id=snippet_pk)
    process_count = len(process_list)

    process_cell_1 = ["C23","G23","O23","X23","AJ23","AS23","BD23","BG23","BI23"]
    process_cell_2 = ["C25","G25","O25","X25","AJ25","AS25","BD25","BG25","BI25"]
    process_cell_3 = ["C27","G27","O27","X27","AJ27","AS27","BD27","BG27","BI27"]
    process_cell_4 = ["C29","G29","O29","X29","AJ29","AS29","BD29","BG29","BI29"]
    process_cell_5 = ["C31","G31","O31","X31","AJ31","AS31","BD31","BG31","BI31"]
    process_cell_6 = ["C33","G33","O33","X33","AJ33","AS33","BD33","BG33","BI33"]

    cell_list = [process_cell_1,process_cell_2,process_cell_3,process_cell_4,process_cell_5,process_cell_6]
    for i in range(process_count):
        process_insert(sheet,process_list[i],cell_list[i])

    # content_typeに、Excelファイル(xlsxファイル)を返すことを表記しています。
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename = report.xlsx"
    # データの書き込みを行なったExcelファイルを保存する
    wb.save(response)
    # 生成したHttpResponseをreturnする
    return response

# excelfile_download内で工程を入力する関数
def process_insert(sheet: openpyxl, process: Process, cell_list: list):
    sheet[cell_list[0]] = process.start_point
    sheet[cell_list[1]] = process.via_point
    sheet[cell_list[2]] = process.end_point
    sheet[cell_list[3]] = process.client
    sheet[cell_list[4]] = process.goods
    sheet[cell_list[5]] = process.load_situation
    if process.is_load_situation != False:
        sheet[cell_list[6]] = "良"
    if process.load_mileage != False:
        sheet[cell_list[7]] = process.load_mileage
    if process.hollow_mileage != False:
       sheet[cell_list[8]] = process.hollow_mileage
