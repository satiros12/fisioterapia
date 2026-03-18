from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
import json


@login_required
def index(request):
    return render(request, "index.html")


@login_required
def exercises_view(request):
    return render(request, "exercises.html")


@login_required
def treatment_plans_view(request):
    if hasattr(request.user, "physiotherapist") and request.user.physiotherapist:
        return render(request, "treatment_plans_manage.html")
    return render(request, "treatment_plans.html")


@login_required
def exercise_detail_view(request, exercise_id):
    return render(request, "exercise_detail.html", {"exercise_id": exercise_id})


@login_required
def calendar_view(request):
    # If physiotherapist, show patient's calendar view, else show own calendar
    if hasattr(request.user, "physiotherapist") and request.user.physiotherapist:
        return render(request, "calendar_physio.html")
    return render(request, "calendar.html")


@login_required
def schedule_view(request):
    # If physiotherapist, show schedule management, else show booking
    if hasattr(request.user, "physiotherapist") and request.user.physiotherapist:
        return render(request, "schedule_manage.html")
    return render(request, "schedule_booking.html")


@login_required
def appointments_view(request):
    # If physiotherapist, show all appointments, else show own
    return render(request, "appointments.html")


@login_required
def messages_view(request):
    return render(request, "messages.html")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_proxy(request, path):
    return JsonResponse({"message": "Use /api/ endpoints directly"}, status=200)
