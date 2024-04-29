from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest
from django.shortcuts import redirect
from .models import Car
from .forms import CarForm
class CarListView(View):
    def get(self, request: HttpRequest):
        cars = Car.objects.all().order_by("-now_mileage")

        return render(
            request,
            "car_list.html",
            {"cars": cars},
        )

car_list = CarListView.as_view()

class CarAddView(View):
    
    def get(self, request):
        return render(
            request,
            "car_add.html",
            {
                "form": CarForm,
            },
        )
    
    def post(self, request):
        req = request.POST
        car_trouble = Car(
            vehicle_number = req.get("vehicle_number_place")
                + " "
                + req.get("vehicle_number_type")
                + " "
                + req.get("vehicle_number_use")
                + " "
                + req.get("vehicle_number_top")
                + "-"
                + req.get("vehicle_number_end"),
            now_mileage = req.get("now_mileage"),
        )
        car_trouble.save()
        return redirect(to='car_list')

car_add = CarAddView.as_view()