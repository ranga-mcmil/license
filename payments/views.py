from django.shortcuts import render, redirect
from licenses.models import LicenseApplication
from .models import Payment
from django.contrib import messages
from django.http import JsonResponse
from payments.ecocash import make_payment
from django.contrib.auth.decorators import login_required
from .forms import PhoneNumberForm
from datetime import datetime, timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta



# Create your views here.
@login_required()
def new(request, id):
    application = LicenseApplication.objects.get(id=id)
    amount = 1

    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)

        if form.is_valid(): 
            phone_number = form.get_info() 
            try:
                payment_status = make_payment(f'Invoice - ID({application.id})', phone_number, request.user.email, amount)['status'] 
            except:
                messages.error(request, 'Something happened, make sure you are connected online')
                return redirect(request.META['HTTP_REFERER'])

            if payment_status == 'paid':
                Payment.objects.create(
                    amount=application.license_type.price,
                    license_application=application,
                    user=application.applicant,
                )

                application.status = 'Approved - (Paid)'
                application.expiry_date = timezone.now() + relativedelta(months=+12)
                application.save()
                messages.success(request, "Payment successful")
                return redirect('licenses:application_detail', application.id)
                         
            elif payment_status == 'sent':
                messages.error(request, 'Ecocash prompt sent, could not get confirmation from user. Please try again')
                return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, 'Error happened, please try again')
                return redirect(request.META['HTTP_REFERER'])
 
        messages.error(request, 'Form not valid')
    else:
        form = PhoneNumberForm()

    context = {
        'form': form,
        'application': application
    }

    return render(request, 'payments/new.html', context)


@login_required()
def payments(request):
    context = {}

    if request.user.user_type == 'Admin':
        payments = Payment.objects.all().order_by('-id')
        context['payments'] = payments
    else:
        payments = Payment.objects.filter(user=request.user).order_by('-date_created')
        context['payments'] = payments

    return render(request, 'payments/payments.html', context)
