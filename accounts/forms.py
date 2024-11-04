from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, USER_TYPE, SEX
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login



# Custom widget
class DateInput(forms.DateInput):
    input_type = 'date'


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'validationCustom08'
        }
    ))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'name': 'password',
            'id': 'validationCustom09'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']

            if not authenticate(username=username, password=password):
                raise forms.ValidationError('Email and password did not match any user in our database')


class UserRegistrationForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'first_name',
            'minlength': "2",
            'maxlength': "50",

        }
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'last_name',
            'minlength': "2",
            'maxlength': "50",

        }
    ))

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'name': 'email',
        }
    ))

    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'address',
        }
    ))

    

    id_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'id_number',
        }
    ))

    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'phone_number',
            'type': 'number'
        }
    ))

    user_type = forms.ChoiceField(required=False, choices=USER_TYPE, widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))


    sex = forms.ChoiceField(required=False, choices=SEX, widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    pic = forms.ImageField(widget=forms.FileInput(
        attrs={
            'id':"file",
            'class': 'form-control image-input',
        }
    ))

    shop_address = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'address',
        }
    ))

    proof_of_residency = forms.ImageField(widget=forms.FileInput(
        attrs={
            'id':"file",
            'class': 'form-control image-input',
        }
    ))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'name': 'password',
            'minlength': "8",
        }
    ))

    password2 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'name': 'password',
            'minlength': "8",
        }
    ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'id_number', 'address', 'sex', 'pic', 'user_type', 'phone_number', 'shop_address', 'proof_of_residency')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match')


class UserUpdateForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'first_name',
            'placeholder': "Enter First Name"
        }
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'last_name',
            'placeholder': "Enter Last Name"
        }
    ))

    id_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'id_number',
        }
    ))

    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'address',
            'placeholder': "Address"
        }
    ))

    sex = forms.ChoiceField(required=False, choices=SEX, widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))
    
    pic = forms.ImageField(widget=forms.FileInput(
        attrs={
            'id':"file",
            'class': 'form-control image-input',
        }
    ))


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'address', 'id_number', 'pic', 'sex')


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control"})