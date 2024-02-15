from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.db.models import Count

from services.models import Service


def home(request):
    top = Service.objects.annotate(num_requests=Count('requestservice')).order_by('-num_requests')[:5]
    return render(request, "main/home.html", {'top_services': top})


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")

