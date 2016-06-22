from django import forms

from .models import Doctor, Patient, Department, Payment
from decimal import Decimal
from django.db.models import Sum


class PatientAdmissionForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['salutation', 'name', 'doctor', 'department', 'house_number', 'street', 'city', 'state', 'pin',
                  'time_admitted',]


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['patient', 'auth_by', 'time_billed', 'medical_exp', 'rent', 'service_charges', 'auth_discharge']

