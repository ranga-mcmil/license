from django.contrib import admin
from .models import LicenseType, LicenseApplication

# Register your models here.
@admin.register(LicenseType)
class LicenseTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(LicenseApplication)
class LicenseApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'license_type', 'status', 'date_created', 'expiry_date')