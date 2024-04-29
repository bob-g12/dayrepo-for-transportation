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
        form = CarForm(request.POST)
        form.save()
        return redirect(to='car_list')

car_add = CarAddView.as_view()