from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def patient_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/accounts/login/?next=" + request.path)

        # Check if impersonating - treat as patient
        if request.session.get("impersonating_user_id"):
            return view_func(request, *args, **kwargs)

        # Check if user is a patient
        if not hasattr(request.user, "patient") or request.user.patient is None:
            messages.error(request, "Esta sección es solo para pacientes.")
            return redirect("/")

        return view_func(request, *args, **kwargs)

    return wrapper


def physiotherapist_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/accounts/login/?next=" + request.path)

        # Physiotherapists cannot access patient-only views
        if request.session.get("impersonating_user_id"):
            messages.error(
                request, "No puedes acceder a esta sección mientras impersonas."
            )
            return redirect("/")

        # Check if user is a physiotherapist
        if (
            not hasattr(request.user, "physiotherapist")
            or request.user.physiotherapist is None
        ):
            messages.error(request, "Esta sección es solo para fisioterapeutas.")
            return redirect("/")

        return view_func(request, *args, **kwargs)

    return wrapper


def get_current_user(request):
    """
    Returns the user being 'acted as' if impersonating, otherwise the actual user.
    """
    if request.session.get("impersonating_user_id"):
        from django.contrib.auth.models import User

        return User.objects.get(id=request.session["impersonating_user_id"])
    return request.user


def get_actual_user(request):
    """
    Returns the actual logged-in user (not the impersonated one).
    """
    return request.user
