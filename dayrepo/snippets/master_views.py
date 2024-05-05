from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
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

def serial_number_divide(car: object):
    if len(str(car.serial_number)) > 2:
        border = len(str(car.serial_number))-2
        str_serial_number = str(car.serial_number)
        serial_number_top = int(str_serial_number[:border])
        serial_number_end = int(str_serial_number[border:])
    else:
        serial_number_top = ""
        serial_number_end = car.serial_number
    return_list = [serial_number_top,serial_number_end]
    return return_list

class CarEditView(View):
    def get(self, request: HttpRequest, car_id: int):
        car = get_object_or_404(Car, pk=car_id)
        serial_number = serial_number_divide(car)
        serial_number_top = serial_number[0]
        serial_number_end = serial_number[1]
        return render(
            request, 
            "car_edit.html", 
            {
                "car":car, 
                "top":serial_number_top,
                "end":serial_number_end,
            }
        )
    def post(self, request: HttpRequest, car_id: int):
        post = get_object_or_404(Car, pk=car_id)
        req = request.POST
        number = int(
            str(req.get("serial_number_top"))
            + str(req.get("serial_number_end"))
        )
        car_trouble = Car(
            id = post.id,
            place_name = req.get("place_name"),
            class_number = req.get("class_number"),
            kana = req.get("kana"),
            serial_number = number,
            now_mileage = req.get("now_mileage"),
        )
        car_trouble.save()
        return redirect(to="car_list")


car_edit = CarEditView.as_view()