from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView
from django.contrib import messages

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer


def register(request):
    return render(request, 'users/register.html')


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.is_customer = 1
        user.is_company = 0
        user.save()
        customer = Customer.objects.create(
            user=user, birth=form.cleaned_data['date_of_birth'])
        customer.save()
        login(self.request, user)
        self.request.session['user_type'] = 'customer'
        self.request.session['user_username'] = form.cleaned_data['username']
        return redirect('/')


class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.is_customer = 0
        user.is_company = 1
        user.save()
        company = Company.objects.create(
            user=user,
            field=form.cleaned_data['field_of_work'],
            rating=0
        )
        company.save()
        login(self.request, user)
        return redirect('/')


def LoginUserView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['email']).first()
            if user is not None and user.check_password(form.cleaned_data['password']):
                login(request, user)
                if user.is_customer:
                    request.session['user_type'] = 'customer'
                    return redirect('/')
                if user.is_company:
                    request.session['user_type'] = 'company'
                    return redirect('/')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})