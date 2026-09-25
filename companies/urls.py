from django.urls import path
from .views import company_dashboard, company_profile

urlpatterns = [
    path("dashboard/", company_dashboard, name="company_dashboard"),
    path("profile/", company_profile, name="company_profile"),
]
