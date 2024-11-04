from django.urls import path
from . import views


app_name = 'payments'
urlpatterns = [
    path('', views.payments, name='payments'),   
    path('new/<int:id>/', views.new, name='new'),   
]