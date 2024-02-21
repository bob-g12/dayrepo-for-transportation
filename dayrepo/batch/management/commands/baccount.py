import sys
sys.path.append('../../../')

from django.core.management.base import BaseCommand
from snippets import models

class Command(BaseCommand):
    help = "テストコマンド"

    def handle(self, *args, **options):
        tmp = models.Account.objects.all()
        for i, t in enumerate(tmp):
            print(i, "個目")
            print("t.id:", t.id)
            print("t.first_name:", t.first_name)
            print("t.last_name:", t.last_name)