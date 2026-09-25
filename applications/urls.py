from django.urls import path

from . import views

urlpatterns = [
    path("", views.application_list, name="application_list"),
    path("create/", views.application_create, name="application_create"),
    path("company/update-status/<int:application_id>/",views.update_application_status,
    name="update_application_status",
),
]