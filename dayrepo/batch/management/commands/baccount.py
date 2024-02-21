import sys
sys.path.append('../../../')

from django.core.management.base import BaseCommand
from snippets import models

class Command(BaseCommand):
    help = "テストコマンド"

    def handle(self, *args, **options):               
        print(args)
        print(options)
        print(options["get"])
        print("options[\"get\"]:", options["get"])
        print("options[\"create\"]:", options["create"])
        print("options[\"del\"]:", options["del"])
        if options["get"] != None and options["get"] == "all": 
            AccountCommand.get_account_all()
            return

        if options["create"] != None and options["create"] == "f":
            print("おいでやす")
            AccountCommand.create_account_in_a_good_way()
            return
        
        if options["del"] != None and options["del"] == "all":
            print("ぽんぽん")
            AccountCommand.all_delete()
            return
    
        print("一致するコマンドが存在しません。")
        
    def add_arguments(self, parser):
        parser.add_argument('--get', nargs='?', default='', type=str)
        parser.add_argument('--create', nargs='?', default='', type=str)
        parser.add_argument('--del', nargs='?', default='', type=str)

class AccountCommand:
    def get_account_all():
        tmp = models.Account.objects.all()
        for i, t in enumerate(tmp):
            print(i+1, "個目")
            print("t.id:", t.id)
            print("t.first_name:", t.first_name)
            print("t.last_name:", t.last_name)
    
    def create_account_in_a_good_way():
        existing_data = models.Account.objects.all()
        n = len(existing_data)+1
        t = models.Account(
            id=n,
            last_name="last_name"+str(n),
            first_name="first_name"+str(n),
            password="password"+str(n),
            is_administrator=True,
            is_approval=True,
        )
        t.save()
        print("以下のデータを作成しました")
        print(t, t.id, t.first_name, t.last_name, t.password, t.is_administrator, t.is_approval)
    
    def all_delete():
        yorn = input("全件削除を行いますか？[Y/n]:")
        if yorn == "y" or yorn == "Y" or yorn == "yes":
            models.Account.objects.all().delete()
            print("Account テーブルの全件削除を行いました")
            return
        
        print("Account テーブルの全件削除を行いませんでした。")
        