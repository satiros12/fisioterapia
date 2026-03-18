from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json


@login_required
def index(request):
    return render(request, "index.html")


@login_required
def exercises_view(request):
    return render(request, "exercises.html")


@login_required
def treatment_plans_view(request):
    return render(request, "treatment_plans.html")


@login_required
def exercise_detail_view(request, exercise_id):
    return render(request, "exercise_detail.html", {"exercise_id": exercise_id})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_proxy(request, path):
    return JsonResponse({"message": "Use /api/ endpoints directly"}, status=200)
