from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User


STATUS = (
    ("Pending", "Pending"),
    ("Expired", "Expired"),
    ("Declined", "Declined"),
    ("Approved - (Pending Payment)", "Approved (Pending Payment)"),
    ("Approved - (Paid)", "Approved (Paid)"),
)

# Create your models here.
class LicenseType(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=20, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f'{self.name} - ${self.price}'



# license application
class LicenseApplication(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    license_type = models.ForeignKey(LicenseType, on_delete=models.CASCADE, related_name="applications")
    notes = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    expiry_date = models.DateTimeField(null=True, blank=True)
