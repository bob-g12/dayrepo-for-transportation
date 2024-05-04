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

class CarView(View):
    
    def get(self, request):
        return render(
            request,
            "car_post.html",
            {
                "form": CarForm,
            },
        )
    
    def post(self, request: HttpRequest):
        req = request.POST
        number = int(
            str(req.get("serial_number_top"))
            + str(req.get("serial_number_end"))
        )
        car_trouble = Car(
            place_name = req.get("place_name"),
            class_number = req.get("class_number"),
            kana = req.get("kana"),
            serial_number = number,
            now_mileage = req.get("now_mileage"),
        )
        car_trouble.save()
        return redirect(to='car_list')

new_car = CarView.as_view()