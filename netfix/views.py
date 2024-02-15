from datetime import datetime
from django.shortcuts import render

from users.models import User, Company
from services.models import Service, RequestService


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    user = User.objects.get(username=name)
    services_requested = RequestService.objects.filter(customer_id=user.id).order_by("-date")
    context = {
        'user': user,
        'user_age': datetime.now().year - user.customer.birth.year,
        'services_requested': services_requested
        }
    return render(request, 'users/profile.html', context)


def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")

    return render(
        request,
        'users/profile.html',
        {'user': user, 'services': services}
    )
