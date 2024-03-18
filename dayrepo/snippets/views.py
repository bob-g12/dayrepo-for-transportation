from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import redirect
from .models import Account, Car, Snippet, DutiesTrouble, Checklist, Process
from .forms import SnippetForm, DutiesTroubleForm, ProcessForm, ChecklistForm


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
        not_submitted_checklist = Checklist.objects.all().order_by("-create_at").filter(is_snippet_make=0)
        

        # トップページのhtmlへ日報データをテンプレートに渡す
        return render(request, "snippet_list.html", {"posts": snippets,"not_posts":not_submitted_checklist})


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
            id = req.get("checklist_id"),
        )
        gasoline = req.get("gasoline_amount")
        if gasoline == "":
            gasoline = 0.0
        oil = req.get("oil")
        if oil == "":
            oil = 0.0

        snippet = Snippet(
            checklist_id = checklist,
            
            # 末尾の [0] について
            # 入力項目のうち同一名のデータは、
            # request.POST に配列で記録され、
            # snippet においては index[0] を使用する
            start_time = req.getlist("start_time")[0],
            end_time = req.getlist("end_time")[0],
            start_point = req.getlist("start_point")[0],
            end_point = req.getlist("end_point")[0],
            start_mileage = req.get("start_mileage"),
            end_mileage = req.get("end_mileage"),
            break_spot = req.get("break_spot"),
            weather = req.get("weather"),
            gasoline_amount = gasoline,
            oil=oil,
            driving_time = req.get("driving_time"),
            non_driving_time = req.get("non_driving_time"),
            break_time = req.get("break_time"),
            is_today_trouble = req.get("is_today_trouble"),
            free_space = req.get("free_space"),
        )
        if snippet.is_today_trouble == "on":
            snippet.is_today_trouble = True
        else:
            snippet.is_today_trouble = False
        snippet.save()
        
        # チェックリストフォーム保存
        checklist = Checklist.objects.get(pk=checklist.id)
        checklist.is_snippet_make = True # 提出済みへ変更
        checklist.save()

        # 業務トラブルフォーム保存
        duties_trouble = DutiesTrouble(
            snippet_id = snippet,
            trouble_situation = req.get("trouble_situation"),
            trouble_cause = req.get("trouble_cause"),
            trouble_support = req.get("trouble_support"),
        )
        duties_trouble.save()

        # 工程テーブルフォーム保存
        form_process_count = len(req.getlist("via_point"))
        for i in range(form_process_count):
            process = Process(
                snippet_id = snippet,
                start_time = req.getlist("start_time")[i + 1],
                end_time = req.getlist("end_time")[i + 1],
                start_point = req.getlist("start_point")[i + 1],
                end_point = req.getlist("end_point")[i + 1],
                via_point = req.getlist("via_point")[i],
                client = req.getlist("client")[i],
                goods = req.getlist("goods")[i],
                load_situation = req.getlist("load_situation")[i],
                load_mileage = req.getlist("load_mileage")[i],
                hollow_mileage = req.getlist("hollow_mileage")[i],
                is_load_situation = req.getlist("is_load_situation")[i],
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

import openpyxl

from django.shortcuts import redirect ,get_object_or_404
    
def excelfile_download(request,snippet_id):
    """
    Excel output from template
    """
    pk=snippet_id
    print("ぴーけー",pk)
    snippet_date = get_object_or_404(Snippet, pk=snippet_id)
    # Excelのテンプレートファイルの読み込み
    wb = openpyxl.load_workbook('../docs/snippet.xlsx')

    sheet = wb['snippet_sheet']
    sheet['E6'] = snippet_date.start_time
    if snippet_date.is_today_trouble == True:
        sheet['AB41'] = "✔"
    sheet['AO8'] = snippet_date.checklist_id.account_id.last_name + " " + snippet_date.checklist_id.account_id.first_name
    
    
    
    print("スニペット",snippet_date.start_time)
    # Excelを返すためにcontent_typeに「application/vnd.ms-excel」をセットします。

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % 'snippet.xlsx'

    # データの書き込みを行なったExcelファイルを保存する
    wb.save(response)

    # 生成したHttpResponseをreturnする
    return response
