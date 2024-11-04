from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django_resized import ResizedImageField

USER_TYPE = (
    ("Applicant", "Applicant"),
    ("Admin", "Admin"),  
)

SEX = (
    ("Male", "Male"),
    ("Female", "Female"),    
)


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    address = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, default='Applicant')
    pic = ResizedImageField(size=[600, 600], crop=['top', 'left'], upload_to='images/')
    sex = models.CharField(max_length=10, choices=SEX)
    shop_address = models.CharField(max_length=50, blank=True, null=True)
    proof_of_residency = ResizedImageField(size=[600, 600], crop=['top', 'left'], upload_to='images/')
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

