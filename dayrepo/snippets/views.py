from django.shortcuts import render
from django.http import HttpResponse, QueryDict
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


class SnippetListView(View):
    def get(self, request):
        # 記録してある投稿の全データを投稿時間を元にソートして表示

        queryset = Snippet.objects.all().order_by("-create_at")
        # トップページのhtmlへ投稿(日報)データをテンプレートに渡す
        return render(request, "snippet_list.html", {"posts": queryset})


snippet_list = SnippetListView.as_view()


# 投稿機能
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
        # formに書いた内容を格納する
        """form = SnippetForm(request.POST)
        form_trouble = DutiesTroubleForm(request.POST)
        form_process = ProcessForm(request.POST)
        form_process2 = ProcessForm({'start_time' : ['02:30:52']})"""
        print(request.POST)
        tmp = request.POST

        # form_duties_trouble = DutiesTroubleForm(request.POST)
        # res_duties_trouble = form_duties_trouble.save()
        # print("res_duties_trouble: ", res_duties_trouble)
        # print("res_duties_trouble: ", res_duties_trouble.id)

        #form_process = ProcessForm(request.POST)
        #res_process = form_process.save()
        form_process = dict(tmp)
        form_process_start_time = tmp.getlist("start_time")[1]
        form_process["start_time"] = [form_process_start_time]
        form_process_end_time = tmp.getlist("end_time")[1]
        form_process["end_time"] = [form_process_end_time]
        form_process_start_point = tmp.getlist("start_point")[1]
        form_process["start_point"] = [form_process_start_point]
        form_process_end_point = tmp.getlist("end_point")[1]
        form_process["end_point"] = [form_process_end_point]
        
        form_process_via_point = tmp.getlist("via_point")[0]
        form_process["via_point"] = [form_process_via_point]
        form_process_client = tmp.getlist("client")[0]
        form_process["client"] = [form_process_client]
        form_process_goods = tmp.getlist("goods")[0]
        form_process["goods"] = [form_process_goods]
        form_process_load_situation = tmp.getlist("load_situation")[0]
        form_process["load_situation"] = [form_process_load_situation]
        form_process_is_load_situation = tmp.getlist("is_load_situation")[0]
        form_process["is_load_situation"] = [form_process_is_load_situation]
        form_process_load_mileage = tmp.getlist("load_mileage")[0]
        form_process["load_mileage"] = [form_process_load_mileage]
        form_process_load_situation = tmp.getlist("load_situation")[0]
        form_process["load_situation"] = [form_process_load_situation]
        print()
        print(form_process)
        return
        # print(dict(tmp))
        form_snippet_start_time = tmp.getlist("start_time")[0]
        print(form_snippet_start_time)
        form_snippet = dict(tmp)
        form_snippet["start_time"] = [form_snippet_start_time]

        form_snippet_end_time = tmp.getlist("end_time")[0]
        print(form_snippet_end_time)
        form_snippet["end_time"] = [form_snippet_end_time]
        print(form_snippet)

        form_snippet_start_point = tmp.getlist("start_point")[0]
        print(form_snippet_start_point)
        form_snippet["start_point"] = [form_snippet_start_point]

        form_snippet_end_point = tmp.getlist("end_point")[0]
        print(form_snippet_end_point)
        form_snippet["end_point"] = [form_snippet_end_point]
        print(QueryDict(form_snippet))

        snippet_save = QueryDict()
        # snippet_save[]

        """# 保存
        form.save()
        form_trouble.save()
        form_process.save()"""
        # トップ画面へ
        return redirect(to="snippet_list")


snippet_post = SnippetView.as_view()
