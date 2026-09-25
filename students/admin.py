from django.contrib import admin
from .models import Student, Document


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "student_id", "university", "program", "year_of_study")
    search_fields = ("student_id", "user__username", "university", "program")
    list_filter = ("year_of_study",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("student", "document_type", "uploaded_at")
    list_filter = ("document_type",)
    search_fields = ("student__user__username", "document_type")
