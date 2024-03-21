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
            {"posts": snippets, "not_posts": not_submitted_checklist},
        )


snippet_list = SnippetListView.as_view()


# snippet画面の表示/POST後処理
class SnippetView(View):
    # 新規入力画面へ
    def get(self, request):
        # 投稿ボタンで投稿ページへ
        return render(
            request,
            "snippet_post.html",
            {
                "form": SnippetForm,
                "form_trouble": DutiesTroubleForm,
                "form_process": ProcessForm,
            },
        )

    # 投稿機能
    def post(self, request):
        req = request.POST

        # スニペットフォーム保存
        # checklists_id挿入のための
        # モデルデータ作成
        checklist = Checklist(
            id=req.get("checklist_id"),
        )
        gasoline = req.get("gasoline_amount")
        if gasoline == "":
            gasoline = 0.0
        oil = req.get("oil")
        if oil == "":
            oil = 0.0

        snippet = Snippet(
            checklist_id=checklist,
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
        )
        if snippet.is_today_trouble == "on":
            snippet.is_today_trouble = True
        else:
            snippet.is_today_trouble = False
        snippet.save()

        # チェックリストフォーム保存
        checklist = Checklist.objects.get(pk=checklist.id)
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

        return redirect(to="snippet_post")


checklist_post = ChecklistView.as_view()


# listページからExcelファイルを出力
def excelfile_download(request, snippet_pk):
    # 引数で受け取った値を変数に代入
    snippet_date = get_object_or_404(Snippet, pk=snippet_pk)
    trouble_date = get_object_or_404(DutiesTrouble, snippet_id=snippet_pk)
    process_date = get_list_or_404(Process, snippet_id=snippet_pk)
    process_count = len(process_date)
    # Excelのテンプレートファイルの読み込み
    wb = openpyxl.load_workbook("./snippets/static/excel/report.xlsx")
    # 入力対象のシート、セルの位置、入寮内容の指定
    sheet = wb["report_sheet"]
    # snippetテーブル
    sheet["E6"] = (
        str(snippet_date.start_time.hour) + ":" + str(snippet_date.start_time.minute)
    )
    sheet["E8"] = (
        str(snippet_date.end_time.hour) + ":" + str(snippet_date.end_time.minute)
    )
    sheet["I6"] = snippet_date.start_point
    sheet["W6"] = snippet_date.end_point
    sheet["Q6"] = (
        str(snippet_date.start_time.hour) + ":" + str(snippet_date.start_time.minute)
    )
    sheet["AE6"] = (
        str(snippet_date.end_time.hour) + ":" + str(snippet_date.end_time.minute)
    )
    weekday = snippet_date.checklist_id.working_day.isoweekday()
    if weekday == 1:
        weekday = "月"
    elif weekday == 2:
        weekday = "火"
    elif weekday == 3:
        weekday = "水"
    elif weekday == 4:
        weekday = "木"
    elif weekday == 5:
        weekday = "金"
    elif weekday == 6:
        weekday = "土"
    elif weekday == 7:
        weekday = "日"
    sheet["A3"] = (
        str(snippet_date.checklist_id.working_day.year)
        + " 年  "
        + str(snippet_date.checklist_id.working_day.month)
        + " 月  "
        + str(snippet_date.checklist_id.working_day.day)
        + " 日  " + "( "
        + weekday
        + " 曜日)  "
        + "天候 ("
        + snippet_date.weather
        + ")"
    )
    sheet["AR3"] = snippet_date.checklist_id.car_id.vehicle_number
    sheet["I9"] = snippet_date.start_mileage
    sheet["S9"] = snippet_date.end_mileage

    today_mileage = snippet_date.end_mileage - snippet_date.start_mileage
    if today_mileage >= 0:
        sheet["AB9"] = today_mileage
    if snippet_date.gasoline_amount != False:
        sheet["E36"] = snippet_date.gasoline_amount
    if snippet_date.oil != False:
        sheet["I36"] = snippet_date.oil

    sheet["BD18"] = (
        str(snippet_date.driving_time.hour)
        + ":"
        + str(snippet_date.driving_time.minute)
    )
    sheet["BD19"] = (
        str(snippet_date.non_driving_time.hour)
        + ":"
        + str(snippet_date.non_driving_time.minute)
    )
    sheet["BD20"] = (
        str(snippet_date.break_time.hour) + ":" + str(snippet_date.break_time.minute)
    )
    work_minute = (
        snippet_date.driving_time.minute + snippet_date.non_driving_time.minute
    )

    work_hour = 0
    if work_minute >= 60:
        work_minute -= 60
        work_hour += 1
    work_hour += snippet_date.driving_time.hour + snippet_date.non_driving_time.hour
    sheet["BG18"] = str(work_hour) + ":" + str(work_minute)
    breek_in_minute = work_minute + snippet_date.break_time.minute
    breek_in_hour = work_hour
    if breek_in_minute >= 60:
        breek_in_minute -= 60
        breek_in_hour += 1
    breek_in_hour += snippet_date.break_time.hour
    sheet["BI18"] = str(breek_in_hour) + ":" + str(breek_in_minute)
    sheet["BF36"] = snippet_date.free_space
    sheet["H21"] = snippet_date.break_spot
    # チェックリストテーブル
    # 左列
    if snippet_date.checklist_id.is_before_trouble == True:
        sheet["AB41"] = "✔"
    if snippet_date.checklist_id.is_tire_damage == True:
        sheet["AB42"] = "✔"
    if snippet_date.checklist_id.is_tire_groove == True:
        sheet["AB43"] = "✔"
    if snippet_date.checklist_id.is_tire_parts == True:
        sheet["AB44"] = "✔"
    if snippet_date.checklist_id.is_radiator == True:
        sheet["AB45"] = "✔"
    if snippet_date.checklist_id.is_brake_oil == True:
        sheet["AB46"] = "✔"
    if snippet_date.checklist_id.is_air_tank == True:
        sheet["AB47"] = "✔"
    if snippet_date.checklist_id.is_engine_oil == True:
        sheet["AB48"] = "✔"
    if snippet_date.checklist_id.is_battery == True:
        sheet["AB49"] = "✔"
    if snippet_date.checklist_id.is_belt == True:
        sheet["AB50"] = "✔"
    if snippet_date.checklist_id.is_parking_brake == True:
        sheet["AB51"] = "✔"
    # 右列
    if snippet_date.checklist_id.is_washer_fluid == True:
        sheet["BJ41"] = "✔"
    if snippet_date.checklist_id.is_engine == True:
        sheet["BJ42"] = "✔"
    if snippet_date.checklist_id.is_air_brake == True:
        sheet["BJ43"] = "✔"
    if snippet_date.checklist_id.is_light == True:
        sheet["BJ44"] = "✔"
    if snippet_date.checklist_id.is_brake_pedal == True:
        sheet["BJ45"] = "✔"
    if snippet_date.checklist_id.is_brake_details == True:
        sheet["BJ46"] = "✔"

    # トラブルテーブル
    if trouble_date.trouble_situation != False:
        sheet["AC36"] = trouble_date.trouble_situation
    if trouble_date.trouble_cause != False:
        sheet["AC37"] = trouble_date.trouble_cause
    if trouble_date.trouble_support != False:
        sheet["AU36"] = trouble_date.trouble_support

    # 工程テーブル
    for i in range(process_count):
        if i == 0:
            sheet["C23"] = process_date[i].start_point
            sheet["G23"] = process_date[i].via_point
            sheet["O23"] = process_date[i].end_point
            sheet["X23"] = process_date[i].client
            sheet["AJ23"] = process_date[i].goods
            sheet["AS23"] = process_date[i].load_situation
            if process_date[i].is_load_situation != False:
                sheet["BD23"] = "良"
            if process_date[i].load_mileage != False:
                sheet["BG23"] = process_date[i].load_mileage
            if process_date[i].hollow_mileage != False:
                sheet["BI23"] = process_date[i].hollow_mileage
        if i == 1:
            sheet["C25"] = process_date[i].start_point
            sheet["G25"] = process_date[i].via_point
            sheet["O25"] = process_date[i].end_point
            sheet["X25"] = process_date[i].client
            sheet["AJ25"] = process_date[i].goods
            sheet["AS25"] = process_date[i].load_situation
            if process_date[i].is_load_situation != False:
                sheet["BD25"] = "良"
            if process_date[i].load_mileage != False:
                sheet["BG25"] = process_date[i].load_mileage
            if process_date[i].hollow_mileage != False:
                sheet["BI25"] = process_date[i].hollow_mileage
        if i == 2:
            sheet["C27"] = process_date[i].start_point
            sheet["G27"] = process_date[i].via_point
            sheet["O27"] = process_date[i].end_point
            sheet["X27"] = process_date[i].client
            sheet["AJ27"] = process_date[i].goods
            sheet["AS27"] = process_date[i].load_situation
            if process_date[i].is_load_situation != False:
                sheet["BD27"] = "良"
            if process_date[i].load_mileage != False:
                sheet["BG27"] = process_date[i].load_mileage
            if process_date[i].hollow_mileage != False:
                sheet["BI27"] = process_date[i].hollow_mileage
        if i == 3:
            sheet["C29"] = process_date[i].start_point
            sheet["G29"] = process_date[i].via_point
            sheet["O29"] = process_date[i].end_point
            sheet["X29"] = process_date[i].client
            sheet["AJ29"] = process_date[i].goods
            sheet["AS29"] = process_date[i].load_situation
            if process_date[i].is_load_situation != False:
                sheet["BD29"] = "良"
            if process_date[i].load_mileage != False:
                sheet["BG29"] = process_date[i].load_mileage
            if process_date[i].hollow_mileage != False:
                sheet["BI29"] = process_date[i].hollow_mileage
        if i == 4:
            sheet["C31"] = process_date[i].start_point
            sheet["G31"] = process_date[i].via_point
            sheet["O31"] = process_date[i].end_point
            sheet["X31"] = process_date[i].client
            sheet["AJ31"] = process_date[i].goods
            sheet["AS31"] = process_date[i].load_situation
            if process_date[i].is_load_situation != False:
                sheet["BD31"] = "良"
            if process_date[i].load_mileage != False:
                sheet["BG31"] = process_date[i].load_mileage
            if process_date[i].hollow_mileage != False:
                sheet["BI31"] = process_date[i].hollow_mileage
        if i == 5:
            sheet["C33"] = process_date[i].start_point
            sheet["G33"] = process_date[i].via_point
            sheet["O33"] = process_date[i].end_point
            sheet["X33"] = process_date[i].client
            sheet["AJ33"] = process_date[i].goods
            sheet["AS33"] = process_date[i].load_situation
            if process_date[i].is_load_situation != False:
                sheet["BD33"] = "良"
            if process_date[i].load_mileage != False:
                sheet["BG33"] = process_date[i].load_mileage
            if process_date[i].hollow_mileage != False:
                sheet["BI33"] = process_date[i].hollow_mileage

    sheet["AO8"] = (
        snippet_date.checklist_id.account_id.last_name
        + " "
        + snippet_date.checklist_id.account_id.first_name
    )
    # Excelを返すためにcontent_typeに「application/vnd.ms-excel」をセットします。
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment; filename = report.xlsx"
    # データの書き込みを行なったExcelファイルを保存する
    wb.save(response)
    # 生成したHttpResponseをreturnする
    return response
