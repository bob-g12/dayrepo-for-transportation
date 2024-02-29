from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import redirect
from .models import Snippet
from .forms import SnippetForm, DutiesTroubleForm, ProcessForm


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


class Snippet_listView(View):
    def get(self, request):
        # 記録してある投稿の全データを投稿時間を元にソートして表示
        queryset = Snippet.objects.all().order_by("account_id")
        # トップページのhtmlへ記録データを乗せ移行
        return render(request, "snippet_list.html", {"posts": queryset})


snippet_list = Snippet_listView.as_view()


# 投稿機能
class SnippetView(View):
    # 新規入力画面へ
    def get(self, request):
        # 投稿ボタンで投稿ページへ
        return render(
            request,
            "snippet_post.html",
            {"form": SnippetForm, "form_trouble": DutiesTroubleForm, "form_process":ProcessForm},
        )

    # 投稿機能
    def post(self, request):
        # formに書いた内容を格納する
        form = SnippetForm(request.POST)
        form_trouble = DutiesTroubleForm(request.POST)
        form_process = ProcessForm(request.POST)
        # 保存する前に一旦取り出す
        post = form.save(commit=False)
        post_trouble = form_trouble.save(commit=False)
        post_process = form_process.save(commit=False)
        # 保存
        post.save()
        post_trouble.save()
        post_process.save()
        # トップ画面へ
        return redirect(to="snippet_list")


snippet_post = SnippetView.as_view()
