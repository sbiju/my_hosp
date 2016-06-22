from django.contrib import admin

from .models import Doctor, Patient, Payment, Department


admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Department)
admin.site.register(Payment)
