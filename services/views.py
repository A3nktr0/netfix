from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from users.models import Company, Customer, User

from .models import Service, RequestService, Rating
from .forms import CreateNewService, RequestServiceForm, RateServiceForm
from django.core.paginator import Paginator


def service_list(request):
    services = Service.objects.all().order_by("-date")
    
    paginator = Paginator(services, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'services/list.html', {'page_obj': page_obj})


def index(request, id):
    service = Service.objects.get(id=id)
    can_rate = False
    try:
        rating_service = Rating.objects.get(service=service)
    except Rating.DoesNotExist:
        rating_service = Rating(service=service)
        rating_service.save()

    if request.user.is_customer and RequestService.objects.filter(service=service, customer=request.user.customer).exists():
        can_rate = True

    if request.method == 'POST':
        form = RateServiceForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            rating_service.rating += rating
            rating_service.save()
            return redirect('/services/')
    else:
        form = RateServiceForm()

    return render(request, 'services/single_service.html', {
        'service': service,
        'can_rate': can_rate,
        'form': form,
        'rating': rating_service.rating})


@login_required
def create(request):
    if request.method == 'POST':
        form = CreateNewService(request.user, request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.company = request.user.company
            service.save()
            return redirect('/services/')
    else:
        form = CreateNewService(request.user)
    return render(request, 'services/create.html', {'form': form})


def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


@login_required
def request_service(request, id):
    service = Service.objects.get(id=id)
    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            request_service = RequestService(
                address=form.cleaned_data['address'],
                time=form.cleaned_data['time'],
                service=service,
                customer=request.user.customer
            )
            request_service.price = request_service.time * service.price_hour
            request_service.save()
            return redirect('/')
    else:
        form = RequestServiceForm()
    return render(request, 'services/request_service.html', {'form': form})


@login_required
def rate_service(request, id):
    service = Service.objects.get(id=id)
    customer = request.user.customer

    # Check if the current user is a customer and has requested the service
    if customer and RequestService.objects.filter(service=service, customer=customer).exists():
        if request.method == 'POST':
            rating = request.POST.get('rating')
            service.rating = rating
            service.save()
            return redirect('/services/')
        else:
            if RequestService.objects.filter(service=service, customer=customer).exists():
                return render(request, 'services/rate_service.html', {'service': service})
    else:
        return redirect('/services/')
