from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def role_required(role):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_staff or request.user.is_superuser:
                return redirect("admin:index")

            profile = getattr(request.user, "profile", None)
            if profile is None or profile.role != role:
                return HttpResponseForbidden(
                    "You do not have permission to access this area."
                )

            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator
