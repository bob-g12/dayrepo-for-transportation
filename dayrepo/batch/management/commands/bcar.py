import sys

sys.path.append("../../../")

from django.core.management.base import BaseCommand
from snippets import models


class Command(BaseCommand):
    help = "テストコマンド"

    def handle(self, *args, **options):
        print("options:", options)
        print('options["get"]:', options["get"])
        print('options["create"]:', options["create"])
        print('options["del"]:', options["del"])
        if options["get"] != None and options["get"] == "all":
            CarCommand.get_car_all()
            return

        if options["create"] != None and options["create"] == "f":
            t = CarCommand()
            t.create_car_in_a_good_way()
            return

        if options["del"] != None and options["del"] == "all":
            CarCommand.all_delete()
            return

        print("一致するコマンドが存在しません。")

    def add_arguments(self, parser):
        parser.add_argument("--get", nargs="?", default="", type=str)
        parser.add_argument("--create", nargs="?", default="", type=str)
        parser.add_argument("--del", nargs="?", default="", type=str)


class CarCommand:
    def get_car_all():
        tmp = models.Car.objects.all()

        if len(tmp) == 0:
            print("現在 Car テーブルのデータは 0 件です。")
            return

        for i, t in enumerate(tmp):
            print(i + 1, "個目")
            print("t.id:", t.id)
            print("t.vehicle_number:", t.vehicle_number)
            print("t.now_mileage:", t.now_mileage)
            print("----")

    def get_vehicle_num_suffix(self, prefix: str, n: int) -> str:
        return prefix + str(n).zfill(4)

    def create_car_in_a_good_way(self):
        existing_data = models.Car.objects.all()
        n = len(existing_data) + 1
        vn = self.get_vehicle_num_suffix("名古屋-123-た-", n)
        t = models.Car(
            id=n,
            vehicle_number=vn,
            now_mileage=1000,
        )
        t.save()
        print("以下のデータを作成しました")
        print(
            t,
            t.id,
            t.vehicle_number,
            t.now_mileage,
        )

    def all_delete():
        yorn = input("Car テーブルの全件削除を行いますか？[Y/n]:")
        if yorn == "y" or yorn == "Y" or yorn == "yes":
            models.Car.objects.all().delete()
            print("Car テーブルの全件削除を行いました。")
            return

        print("Car テーブルの全件削除を行いませんでした。")
