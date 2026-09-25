from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, render

from applications.models import Application
from accounts.decorators import role_required

from .forms import CompanyProfileForm
from .models import Company


@role_required("Company")
def company_dashboard(request):
    try:
        profile = request.user.company_profile
    except Company.DoesNotExist:
        profile = None

    opportunities = []
    applications = []

    if profile:
        opportunities = profile.opportunities.annotate(
            application_count=Count("applications")
        ).order_by("-created_at")

        applications = (
            Application.objects
            .filter(opportunity__company=profile)
            .select_related("student", "opportunity")
            .order_by("-applied_at")
        )

    return render(request, "companies/dashboard.html", {
        "profile": profile,
        "opportunities": opportunities,
        "applications": applications,
    })


@role_required("Company")
def company_profile(request):
    try:
        profile = request.user.company_profile
    except Company.DoesNotExist:
        profile = None

    if request.method == "POST":
        form = CompanyProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()

            messages.success(
                request,
                "Your company profile has been saved.",
            )
            return redirect("company_dashboard")
    else:
        form = CompanyProfileForm(instance=profile)

    return render(request, "companies/profile.html", {
        "profile": profile,
        "form": form,
    })