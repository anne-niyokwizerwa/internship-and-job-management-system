from django.urls import path

from . import views


urlpatterns = [
    path("", views.opportunity_list, name="opportunity_list"),

    path(
        "<int:opportunity_id>/",
        views.opportunity_detail,
        name="opportunity_detail",
    ),

    path(
        "edit/<int:opportunity_id>/",
        views.opportunity_edit,
        name="opportunity_edit",
    ),

    path(
        "delete/<int:opportunity_id>/",
        views.opportunity_delete,
        name="opportunity_delete",
    ),

    path("create/", views.opportunity_create, name="opportunity_create"),
]