from __future__ import unicode_literals

from django.utils.translation import gettext as _
from django.db import models
from decimal import Decimal
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
import datetime

CHOICES = (
        ('MR', 'Mr'),
        ('MRS', 'Mrs'),
        ('MISS', 'Miss'),
    )


class Doctor(models.Model):
    salutation = models.CharField(choices=CHOICES, blank=True, null=True, max_length=6)
    name = models.CharField(max_length=120, blank=True, null=True)
    degree = models.CharField(max_length=25, blank=True, null=True)
    speciality = models.CharField(max_length=120, blank=True, null=True)
    house_number = models.CharField(max_length=120, blank=True, null=True)
    street = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    state = models.CharField(max_length=120, blank=True, null=True)
    pin = models.PositiveIntegerField(blank=True, null=True)

    def __unicode__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('hospital:doctor_detail', kwargs={'pk': self.pk})


class Patient(models.Model):
    doctor = models.ForeignKey(Doctor, blank=True, null=True)
    salutation = models.CharField(choices=CHOICES, blank=True, null=True, max_length=6)
    name = models.CharField(max_length=120, blank=True, null=True, unique=True)
    age = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    house_number = models.CharField(max_length=120, blank=True, null=True)
    street = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    state = models.CharField(max_length=120, blank=True, null=True)
    pin = models.PositiveIntegerField(blank=True, null=True)
    department = models.ForeignKey('Department', null=True)
    time_admitted = models.DateTimeField(default=datetime.datetime.now, null=True)
    time_discharged = models.DateTimeField(null=True, blank=True)
    is_approved_discharge =  models.BooleanField(default=False, verbose_name='Approve?')
    is_discharged = models.BooleanField(default=False, verbose_name='Discharge?')

    class Meta:
        ordering = ["-time_admitted"]

    def __unicode__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('hospital:patient_detail', kwargs={'pk': self.pk})

    def get_approve_url(self):
        return reverse('hospital:discharge_approve', kwargs={'pk': self.pk})

    def get_discharge_url(self):
        return reverse('hospital:discharge_complete', kwargs={'pk': self.pk})


class Payment(models.Model):
    patient = models.ForeignKey(Patient, blank=True)
    auth_by = models.ForeignKey(Doctor, related_name='payment', blank=True, null=True)
    time_billed = models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)
    medical_exp = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
    rent = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
    service_charges = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=25, decimal_places=2, default=9.99)
    tax_total = models.DecimalField(max_digits=25, decimal_places=2, default=9.99)
    total = models.DecimalField(max_digits=25, decimal_places=2,  default=9.99)
    auth_discharge = models.BooleanField(default=False)

    class Meta:
        ordering = ["-time_billed"]

    def __unicode__(self):
        return str(self.total)

    def get_absolute_url(self):
        return reverse('hospital:payment_detail', kwargs={'pk': self.pk})


def total_reciever(sender, instance, *args, **kwargs):
    medical_exp = instance.medical_exp
    rent = instance.rent
    service_charges = instance.service_charges
    subtotal = Decimal(rent)+Decimal(service_charges)+Decimal(medical_exp)
    instance.subtotal = subtotal
    tax_total = subtotal * Decimal(0.15)
    instance.tax_total = tax_total
    total = round(Decimal(subtotal) + Decimal(tax_total), 2)
    instance.total = total

pre_save.connect(total_reciever, sender=Payment)


class Department(models.Model):
    department = models.CharField(max_length=20, blank=True, null=True)
    no_of_wards = models.IntegerField(default=10)

    def __unicode__(self):
        return str(self.department)

