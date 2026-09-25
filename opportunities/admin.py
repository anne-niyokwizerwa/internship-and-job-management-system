from django.contrib import admin
from .models import Opportunity


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "opportunity_type", "location", "deadline", "status")
    list_filter = ("opportunity_type", "status")
    search_fields = ("title", "company__company_name", "location")
