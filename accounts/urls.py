from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("password/", views.password_change_view, name="password_change"),
    path(
        "password/done/", views.password_change_done_view, name="password_change_done"
    ),
]
