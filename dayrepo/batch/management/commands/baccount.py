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
        print("options[\"get\"]:", options["get"] == "")
        if options["get"] != None and options["get"] == "all": 
            AccountCommand.get_account_all()
            return
    
        print("一致するコマンドが存在しません。")
        
    def add_arguments(self, parser):
        parser.add_argument('--get', nargs='?', default='', type=str)

class AccountCommand:
    def get_account_all():
        tmp = models.Account.objects.all()
        for i, t in enumerate(tmp):
            print(i+1, "個目")
            print("t.id:", t.id)
            print("t.first_name:", t.first_name)
            print("t.last_name:", t.last_name)