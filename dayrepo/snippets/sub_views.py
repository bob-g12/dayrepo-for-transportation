from django.shortcuts import render
from django.views.generic import View
from .models import Account, Car, Snippet, DutiesTrouble, Checklist, Process

class VehicleListView(View):
    def get(self, request):
        # 記録してある投稿の全データを投稿時間を元にソートして表示
        # snippets は存在する時点で提出済みとみなす
        cars = Car.objects.all()

        # トップページのhtmlへ日報データをテンプレートに渡す
        return render(
            request,
            "vehicle_top_page.html",
            {"vehicles": cars},
        )

vehicle_list = VehicleListView.as_view()