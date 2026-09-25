
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import RegisterForm
from .models import Profile

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect("admin:index")

        role = getattr(getattr(request.user, "profile", None), "role", None)
        if role == "Student":
            return redirect("student_dashboard")
        if role == "Company":
            return redirect("company_dashboard")
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(
                request,
                "You have logged in successfully."
            )

            if user.is_staff or user.is_superuser:
                return redirect("admin:index")

            role = getattr(getattr(user, "profile", None), "role", None)
            if role == "Student":
                return redirect("student_dashboard")

            if role == "Company":
                return redirect("company_dashboard")

            return redirect("home")

        messages.error(request, "Invalid username or password.")

    requested_role = request.GET.get("role", "")
    return render(request, "accounts/login.html", {
        "requested_role": requested_role,
    })



def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        role = request.POST.get("role")

        if role not in dict(Profile.ROLE_CHOICES):
            form.add_error(None, "Choose whether this account is for a student or company.")

        if form.is_valid() and role in dict(Profile.ROLE_CHOICES):
            user = form.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={"role": role}
            )

            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully."
            )

            if role == "Student":
                return redirect("student_profile")

            elif role == "Company":
                return redirect("company_profile")

            return redirect("home")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )

def logout_view(request):
    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("home")