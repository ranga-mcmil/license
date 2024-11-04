from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, UserRegistrationForm, UserUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from licenses.models import LicenseApplication
from licenses import utils
from django_middleware_global_request import get_request


# Create your views here.
@login_required()
def dashboard(request):
    print('?????????????????????????')
    request = get_request()
    print('REQUEST', request)
    print('>>>>>>>>>>>>>>>>>')


    utils.check_if_expired(request.user)
    if request.user.user_type == 'Admin':
        pending = LicenseApplication.objects.filter(status='Pending').count()
        declined = LicenseApplication.objects.filter(status='Declined').count()
        pending_payment = LicenseApplication.objects.filter(status='Approved - (Pending Payment)').count()
        paid = LicenseApplication.objects.filter(status='Approved - (Paid)').count()
        expired = LicenseApplication.objects.filter(status='Expired').count()
    else:
        pending = LicenseApplication.objects.filter(applicant=request.user, status='Pending').count()
        declined = LicenseApplication.objects.filter(applicant=request.user, status='Declined').count()
        pending_payment = LicenseApplication.objects.filter(applicant=request.user, status='Approved - (Pending Payment)').count()
        paid = LicenseApplication.objects.filter(applicant=request.user, status='Approved - (Paid)').count()
        expired = LicenseApplication.objects.filter(applicant=request.user, status='Expired').count()

    context = {
        'pending': pending,
        'declined': declined,
        'pending_payment': pending_payment,
        'paid': paid,
        'expired': expired
    }
    
    return render(request, 'accounts/dashboard.html', context)


class PasswordChangeView(PasswordChangeView):
    form_class = MyPasswordChangeForm
    template_name = "registration/password_change_form.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Password updated successfully")
        return super(PasswordChangeView, self).form_valid(form)

def login_view(request):
    if request.POST:
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'You are now logged in as {user.get_full_name()}')
            return redirect('accounts:dashboard')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, f'Registration Successful. You are now logged in as {user.get_full_name()}')
            return redirect('accounts:dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes Saved Successfully")
            return redirect('accounts:dashboard')
        messages.warning(request, "Something happened")
    else:
        form = UserUpdateForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'accounts/profile_edit.html', context)


def my_logout(request):
    logout(request)
    messages.success(request, "You have successfully signed out")
    return redirect('accounts:dashboard')


@login_required()
def notifications_(request):
    user = request.user  
    user.notifications.unread().mark_all_as_read()
    notifications = user.notifications.read() 
    
    context = {
        'notifications': notifications
    }
    return render(request, 'accounts/notifications_.html', context)