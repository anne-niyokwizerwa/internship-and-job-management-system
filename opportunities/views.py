from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from companies.models import Company

from .forms import OpportunityForm
from .models import Opportunity


def opportunity_list(request):
    opportunities = (
        Opportunity.objects
        .select_related("company")
        .filter(status=True)
    )

    search_query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()

    if search_query:
        opportunities = opportunities.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(location__icontains=search_query)
            | Q(company__company_name__icontains=search_query)
        )

    if selected_category:
        opportunities = opportunities.filter(category=selected_category)

    return render(request, "opportunities/list.html", {
        "opportunities": opportunities.order_by("-created_at"),
        "search_query": search_query,
        "selected_category": selected_category,
        "categories": Opportunity.CATEGORIES,
    })


def opportunity_detail(request, opportunity_id):
    opportunity = get_object_or_404(
        Opportunity.objects.select_related("company"),
        id=opportunity_id,
        status=True,
    )

    return render(request, "opportunities/detail.html", {
        "opportunity": opportunity,
    })


@role_required("Company")
def opportunity_create(request):
    try:
        company = request.user.company_profile
    except Company.DoesNotExist:
        messages.error(
            request,
            "Create your company profile before posting an opportunity.",
        )
        return redirect("company_profile")

    if request.method == "POST":
        form = OpportunityForm(request.POST)

        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.company = company
            opportunity.save()

            messages.success(request, "Opportunity created successfully.")
            return redirect("company_dashboard")
    else:
        form = OpportunityForm()

    return render(request, "opportunities/create.html", {"form": form})


@role_required("Company")
def opportunity_edit(request, opportunity_id):
    company = get_object_or_404(Company, user=request.user)

    opportunity = get_object_or_404(
        Opportunity,
        id=opportunity_id,
        company=company,
    )

    if request.method == "POST":
        form = OpportunityForm(request.POST, instance=opportunity)

        if form.is_valid():
            form.save()
            messages.success(request, "Opportunity updated successfully.")
            return redirect("company_dashboard")
    else:
        form = OpportunityForm(instance=opportunity)

    return render(request, "opportunities/edit.html", {
        "form": form,
        "opportunity": opportunity,
    })


@role_required("Company")
def opportunity_delete(request, opportunity_id):
    company = get_object_or_404(Company, user=request.user)

    opportunity = get_object_or_404(
        Opportunity,
        id=opportunity_id,
        company=company,
    )

    if request.method == "POST":
        opportunity.delete()
        messages.success(request, "Opportunity deleted successfully.")
        return redirect("company_dashboard")

    return render(request, "opportunities/delete.html", {
        "opportunity": opportunity,
    })