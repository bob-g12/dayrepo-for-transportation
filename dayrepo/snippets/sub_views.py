from django.shortcuts import render
from django.views.generic import View
from .models import Account, Car

class VehicleListView(View):
    def get(self, request):
        cars = Car.objects.all()

        return render(
            request,
            "vehicle_list.html",
            {"vehicles": cars},
        )

vehicle_list = VehicleListView.as_view()