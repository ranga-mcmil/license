from django.shortcuts import render, redirect
from .forms import LicenseTypeForm, LicenseApplicationForm
from .models import LicenseType, LicenseApplication
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from notifications.signals import notify
from datetime import datetime, timedelta
from django.utils import timezone
from . import utils

# Create your views here.
@login_required()
def license_type_new(request):
    if request.method == 'POST':
        form = LicenseTypeForm(data=request.POST)

        if form.is_valid():
            new_license = form.save()
            messages.success(request, "Saved successfully")
            return redirect('licenses:license_type_list')
        messages.error(request, 'Form not valid')
    else:
        form = LicenseTypeForm()

    context = {
        'form': form,
    }

    return render(request, 'licenses/license_type_new.html', context)


@login_required()
def license_type_list(request):
    license_types = LicenseType.objects.all().order_by('-id')

    context = {
        'license_types': license_types
    }

    return render(request, 'licenses/license_type_list.html', context)


@login_required()
def license_type_edit(request, id):

    license_type = LicenseType.objects.get(id=id)
    if request.method == 'POST':
        form = LicenseTypeForm(request.POST, instance=license_type)

        if form.is_valid():
            form.save()
            messages.success(request, 'Changes saved')
            return redirect('licenses:license_type_list')
        messages.error(request, 'Error saving changes')
    else:
        form = LicenseTypeForm(instance=license_type)

    context = {
        'form': form,
    }

    return render(request, 'licenses/license_type_edit.html', context)


@login_required()
def license_type_delete(request, id):
    if request.user.user_type == 'Admin':
        license_type = LicenseType.objects.get(id=id)
        license_type.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('licenses:license_type_list')
    else:
        messages.error(request, 'You do not have rights to perform this action')
        return redirect('accounts:dashboard')


# Applications ===============
@login_required()
def applications(request):
    utils.check_if_expired(request.user)
    try:
        filter_val = request.GET['f']
        if request.user.user_type == 'Admin':
            applications = LicenseApplication.objects.filter(status=filter_val).order_by('-id')
        else:
            applications = LicenseApplication.objects.filter(applicant=request.user, status=filter_val).order_by('-id')

    except:
        if request.user.user_type == 'Admin':
            applications = LicenseApplication.objects.all().order_by('-id')
        else:
            applications = LicenseApplication.objects.filter(applicant=request.user).order_by('-id')

    
    context = {
        'applications': applications
    }

    return render(request, 'licenses/applications.html', context)


@login_required()
def application_detail(request, id):
    application = LicenseApplication.objects.get(id=id)

    context = {
        'application': application,
    }

    return render(request, 'licenses/application_detail.html', context)



@login_required()
def application_new(request):
    if request.method == 'POST':
        form = LicenseApplicationForm(data=request.POST)

        if form.is_valid():
            new_application = form.save(commit=False)
            new_application.applicant = request.user
            new_application.save()
            messages.success(request, "Saved successfully")
            return redirect('licenses:application_detail', new_application.id)
        messages.error(request, 'Form not valid')
    else:
        form = LicenseApplicationForm()

    context = {
        'form': form,
    }

    return render(request, 'licenses/application_new.html', context)


@login_required()
def application_delete(request, id):
    application = LicenseApplication.objects.get(id=id)
    application.delete()
    messages.success(request, 'Successfully deleted')
    return redirect('licenses:applications')
    
@login_required()
def approve(request, id):
    application = LicenseApplication.objects.get(id=id)
    application.status = 'Approved - (Pending Payment)'
    application.save()
    notify.send(request.user, recipient=application.applicant, verb='Approve', action_object=application, description=f'Your application has been approved. Make payment to complete process')
    messages.success(request, 'Successfully Approved')
    return redirect('licenses:applications')

@login_required()
def decline(request, id):
    application = LicenseApplication.objects.get(id=id)
    application.status = 'Declined'
    application.save()
    notify.send(request.user, recipient=application.applicant, verb='Decline', action_object=application, description=f'Your application has been declined.')
    messages.warning(request, 'Application Declined')
    return redirect('licenses:applications')