"""URL configuration for config project."""
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.http import HttpResponse


def home(request):
    return render(request, "home.html")

    return HttpResponse("Welcome to Internship Job Management System")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("students/", include("students.urls")),
    path("companies/", include("companies.urls")),
    path("opportunities/", include("opportunities.urls")),
    path("applications/", include("applications.urls")),
]
