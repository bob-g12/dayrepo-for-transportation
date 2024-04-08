from django.urls import path
from snippets import views

urlpatterns = [
    path("new/", views.snippet_new,name="snippet_new"),
    path("new/checklist/", views.snippet_new_checklist,name="snippet_new_checklist"),
    path("<int:snippet_id>/", views.snippet_update,name="snippet_update"),
    path("<int:snippet_id>/checklist/", views.snippet_update_checklist,name="snippet_update_checklist"),
    path("car/", views.pre_car_registration,name="pre_car_registration"),
    path("car/new/", views.car_registration,name="car_registration"),
    path("employee/", views.get_employee,name="get_employee"),
    path("list/", views.snippet_list,name="snippet_list"),
    path("post/<int:checklist_id>/", views.snippet_post,name="snippet_post"),
    path("checklist/", views.checklist_post,name="checklist_post"),
    path("edit/<int:snippet_id>/", views.snippet_edit,name="snippet_edit"),
    path("edit/checklist/<int:checklist_id>/", views.checklist_edit,name="checklist_edit"),
    path("excel/<int:snippet_pk>/", views.excelfile_download,name="excelfile_download"),
]