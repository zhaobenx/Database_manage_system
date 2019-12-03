from django.contrib import admin

# Register your models here.
from .models import Hospital, Department, Physician, Patient, PatientTreatment, Treatment,Disease

class HospitalAdmin(admin.ModelAdmin):
    list_display = ['hid', 'hname','hst_address','hst_city', 'hstate', 'hzip']

admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Department)
admin.site.register(Physician)
admin.site.register(Patient)
admin.site.register(PatientTreatment)
admin.site.register(Treatment)
admin.site.register(Disease)