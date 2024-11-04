from datetime import datetime, timedelta
from django.utils import timezone
from .models import LicenseType, LicenseApplication
from notifications.signals import notify

def check_if_expired(user):
    
    applications = LicenseApplication.objects.all()

    for application in applications:
        try:
            if application.status == "Approved - (Paid)" and application.expiry_date < timezone.now():    
                application.status = "Expired"
                application.save()
                notify.send(user, recipient=application.applicant, verb='Expired', action_object=application, description=f'Your license has expired. Please renew')

        except:
            continue

