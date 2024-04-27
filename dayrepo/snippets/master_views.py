from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest
from .models import Car

class CarListView(View):
    def get(self, request: HttpRequest):
        cars = Car.objects.all().order_by("-now_mileage")

        return render(
            request,
            "car_list.html",
            {"cars": cars},
        )

car_list = CarListView.as_view()