from django.db import models
from licenses.models import LicenseApplication
from accounts.models import User


class Payment(models.Model):
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=20)
    license_application = models.ForeignKey(LicenseApplication, on_delete=models.CASCADE, related_name="payments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    date_created = models.DateTimeField(auto_now_add=True)