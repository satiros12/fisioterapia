from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy


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
