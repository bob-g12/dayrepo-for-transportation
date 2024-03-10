from django.contrib import admin

from .models import Account,Car,Checklist,Snippet,DutiesTrouble,Process
# Register your models here.
admin.site.register(Account)

admin.site.register(Car)

admin.site.register(Checklist)

admin.site.register(Snippet)

admin.site.register(DutiesTrouble)

admin.site.register(Process)