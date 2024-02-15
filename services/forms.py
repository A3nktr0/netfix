from django import forms

from users.models import Company
from .models import Service


class CreateNewService(forms.ModelForm):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, min_value=0.00)
    field = forms.ChoiceField(required=True)

    def __init__(self, user, *args, **kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        company = Company.objects.get(user=user)

        # adding choices to fields
        if company.field == 'All in One':
            self.fields['field'].choices = [
                ('Air Conditioner', 'Air Conditioner'),
                ('Carpentry', 'Carpentry'),
                ('Electricity', 'Electricity'),
                ('Gardening', 'Gardening'),
                ('Home Machines', 'Home Machines'),
                ('House Keeping', 'House Keeping'),
                ('Interior Design', 'Interior Design'),
                ('Locks', 'Locks'),
                ('Painting', 'Painting'),
                ('Plumbing', 'Plumbing'),
                ('Water Heaters', 'Water Heaters')
            ]
        else:
            self.fields['field'].choices = [(company.field, company.field)]

        # adding placeholders to form fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'

        self.fields['name'].widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Service
        fields = ['name', 'description', 'price_hour', 'field']


class RequestServiceForm(forms.Form):
    address = forms.CharField(max_length=100)
    time = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        super(RequestServiceForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['placeholder'] = 'Enter Address'
        self.fields['time'].widget.attrs['placeholder'] = 'Enter Time in Hours'


class RateServiceForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    
    def __init__(self, *args, **kwargs):
        super(RateServiceForm, self).__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs['placeholder'] = 'Enter Rating'