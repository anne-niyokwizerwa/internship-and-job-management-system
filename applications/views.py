from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from companies.models import Company
from opportunities.models import Opportunity
from students.models import Student

from .forms import ApplicationForm
from .models import Application


@role_required("Student")
def application_create(request):
    student = get_object_or_404(Student, user=request.user)

    opportunity_id = (
        request.GET.get("opportunity")
        or request.POST.get("opportunity")
    )

    opportunity = get_object_or_404(
        Opportunity,
        pk=opportunity_id,
        status=True,
    )

    if request.method == "POST":
        form = ApplicationForm(
            request.POST,
            request.FILES,
        )
    else:
        form = ApplicationForm()

    if "opportunity" in form.fields:
        form.fields["opportunity"].queryset = Opportunity.objects.filter(
            pk=opportunity.pk,
        )
        form.initial["opportunity"] = opportunity.pk

    already_applied = Application.objects.filter(
        student=student,
        opportunity=opportunity,
    ).exists()

    if already_applied:
        messages.info(
            request,
            "You have already applied for this opportunity.",
        )
        return redirect("application_list")

    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.student = student
        application.opportunity = opportunity
        application.save()

        messages.success(
            request,
            "Application submitted successfully.",
        )
        return redirect("application_list")

    return render(request, "applications/create.html", {
        "form": form,
        "opportunity": opportunity,
    })


@role_required("Student")
def application_list(request):
    student = get_object_or_404(Student, user=request.user)

    applications = (
        Application.objects
        .filter(student=student)
        .select_related("opportunity", "opportunity__company")
        .order_by("-applied_at")
    )

    return render(request, "applications/application_list.html", {
        "applications": applications,
    })


@role_required("Company")
def update_application_status(request, application_id):
    if request.method != "POST":
        return redirect("company_dashboard")

    company = get_object_or_404(
        Company,
        user=request.user,
    )

    application = get_object_or_404(
        Application,
        id=application_id,
        opportunity__company=company,
    )

    status = request.POST.get("status")

    if status in dict(Application.STATUS_CHOICES):
        application.status = status
        application.save(update_fields=["status"])

        messages.success(
            request,
            "Application status updated.",
        )

    return redirect("company_dashboard")