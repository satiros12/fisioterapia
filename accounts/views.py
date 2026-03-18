from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .decorators import physiotherapist_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    # Clear impersonation on logout
    if "impersonating_user_id" in request.session:
        del request.session["impersonating_user_id"]
    if "impersonating_username" in request.session:
        del request.session["impersonating_username"]
    logout(request)
    return redirect("/accounts/login/")


@login_required
def password_change_view(request):
    from django.contrib.auth.views import PasswordChangeView
    from django.urls import reverse_lazy

    class CustomPasswordChangeView(PasswordChangeView):
        template_name = "accounts/password_change.html"
        success_url = reverse_lazy("password_change_done")

    return CustomPasswordChangeView.as_view()(request)


@login_required
def password_change_done_view(request):
    from django.contrib.auth.views import PasswordChangeDoneView

    class CustomPasswordChangeDoneView(PasswordChangeDoneView):
        template_name = "accounts/password_change_done.html"

    return CustomPasswordChangeDoneView.as_view()(request)


@login_required
@physiotherapist_required
def patients_list(request):
    """List all patients for physiotherapist to manage."""
    from patients.models import Patient

    patients = Patient.objects.select_related("user").all()
    return render(request, "accounts/patients_list.html", {"patients": patients})


@login_required
@physiotherapist_required
def impersonate_patient(request, user_id):
    """Allow physiotherapist to act as a patient."""
    from patients.models import Patient

    try:
        patient = Patient.objects.get(user_id=user_id)
        request.session["impersonating_user_id"] = patient.user_id
        request.session["impersonating_username"] = (
            patient.user.get_full_name() or patient.user.username
        )
        messages.success(
            request,
            f"Ahora estás actuando como {request.session['impersonating_username']}",
        )
    except Patient.DoesNotExist:
        messages.error(request, "Paciente no encontrado.")

    return redirect("/")


@login_required
def stop_impersonate(request):
    """Stop impersonating and return to physiotherapist view."""
    if "impersonating_user_id" in request.session:
        del request.session["impersonating_user_id"]
    if "impersonating_username" in request.session:
        del request.session["impersonating_username"]
    messages.success(request, "Has vuelto a tu sesión de fisioterapeuta.")
    return redirect("/pacientes")
