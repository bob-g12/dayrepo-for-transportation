from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.views.generic import View
from django.shortcuts import redirect
from .models import Account, Car, Snippet, DutiesTrouble, Checklist, Process
from .forms import SnippetForm, DutiesTroubleForm, ProcessForm, ChecklistForm
from django.db import models


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

        queryset = Snippet.objects.all().order_by("-create_at")
        # トップページのhtmlへ投稿(日報)データをテンプレートに渡す
        return render(request, "snippet_list.html", {"posts": queryset})


snippet_list = SnippetListView.as_view()


# snippet投稿機能
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
        print(request.POST)
        req = request.POST

        # Snippets form
        account = Account(
            id = req.get("account_id"),
        )
        car = Car(
            id = req.get("car_id"),
        )
        gasoline = req.get("gasoline_amount")
        if gasoline == "":
            gasoline = 0.0

        oil = req.get("oil")
        if oil == "":
            oil = 0.0
        snippet = Snippet(
            # account, car について
            # 別テーブルからデータを取得する際に
            # モデルデータで挿入する必要がある
            account_id=account,
            car_id = car,
            # 末尾の [0] について
            # 入力項目のうち同一名のデータは、
            # request.POST に配列で記録され、
            # snippet においては index[0] を使用する
            start_time = req.getlist("start_time")[0],
            end_time = req.getlist("end_time")[0],
            start_point = req.getlist("start_point")[0],
            end_point = req.getlist("end_point")[0],
            create_day = req.get("create_day"),
            start_mileage = req.get("start_mileage"),
            end_mileage = req.get("end_mileage"),
            break_spot = req.get("break_spot"),
            weather = req.get("weather"),
            gasoline_amount = gasoline,
            oil=oil,
            driving_time = req.get("driving_time"),
            non_driving_time = req.get("non_driving_time"),
            break_time = req.get("break_time"),
            free_space = req.get("free_space"),
        )
        snippet.save()

        # DutiesTrouble form
        duties_trouble = DutiesTrouble(
            snippet_id = snippet,
            trouble_situation = req.get("trouble_situation"),
            trouble_cause = req.get("trouble_cause"),
            trouble_support = req.get("trouble_support"),
        )
        duties_trouble.save()

        # Process form
        form_process_count = len(req.getlist("via_point"))
        print(form_process_count)
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

# checklist投稿機能
class ChecklistView(View):
    # 新規入力画面
    def get(self, request):
        # 投稿ボタンで投稿ページへ
        return render(
            request,
            "snippet_checklist.html",
            {
                "form": ChecklistForm,
            },
        )

    # 投稿機能
    def post(self, request):

        # Checklist Form
        checklist = ChecklistForm(request.POST)
        # ※Process formとのbool入力処理の違い
        # Process formではboolの入力値が"on"/"off"になっていたが、
        # formの引数にrequest.POSTを指定した場合、"True"/"False"で
        # 登録してくれる(結論、変換しなくていい)
        checklist.save()
        
        return redirect(to="snippet_post")
    
checklist_post = ChecklistView.as_view()