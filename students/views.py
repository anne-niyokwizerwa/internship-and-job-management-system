from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.decorators import role_required

from .forms import StudentProfileForm
from .models import Student


@role_required("Student")
def student_dashboard(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return redirect("student_profile")

    return render(
        request,
        "students/dashboard.html",
        {
            "student": student,
        }
    )


@role_required("Student")
def student_profile(request):
    try:
        profile = request.user.student_profile
    except Student.DoesNotExist:
        profile = None

    form = StudentProfileForm(
        request.POST or None,
        instance=profile
    )

    if request.method == "POST" and form.is_valid():
        student = form.save(commit=False)
        student.user = request.user
        student.save()

        messages.success(
            request,
            "Your student profile has been saved successfully!"
        )

        return redirect("opportunity_list")

    return render(
        request,
        "students/profile.html",
        {
            "form": form
        }
    )