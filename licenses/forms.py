from django import forms
from .models import LicenseType, LicenseApplication

class LicenseTypeForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'first_name',
        }
    ))

    price = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': "number",
            'step': ".01"
        }
    ))

    class Meta:
        model = LicenseType
        fields = ('name', 'price')


class LicenseApplicationForm(forms.ModelForm):

    license_type = forms.ModelChoiceField(queryset=LicenseType.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    notes = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'id': 'description',
        }
    ))


    class Meta:
        model = LicenseApplication
        fields = ('license_type', 'notes')