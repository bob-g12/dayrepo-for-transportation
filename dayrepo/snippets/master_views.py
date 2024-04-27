from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest
from .models import Car

class VehicleListView(View):
    def get(self, request: HttpRequest):
        cars = Car.objects.all().order_by("-now_mileage")

        return render(
            request,
            "vehicle_list.html",
            {"vehicles": cars},
        )

vehicle_list = VehicleListView.as_view()