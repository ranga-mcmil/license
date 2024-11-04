from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'licenses'

urlpatterns = [
    path('type/new/', views.license_type_new, name='license_type_new'),
    path('types/', views.license_type_list, name='license_type_list'),
    path('types/edit/<int:id>', views.license_type_edit, name='license_type_edit'),
    path('types/delete/<int:id>/', views.license_type_delete, name='license_type_delete'),

    path('applications/', views.applications, name='applications'),
    path('applications/new/', views.application_new, name='application_new'),
    path('applications/detail/<int:id>/', views.application_detail, name='application_detail'),
    # path('applications/edit/<int:id>/', views.application_edit, name='application_edit'),
    path('applications/delete/<int:id>/', views.application_delete, name='application_delete'),
    path('applications/approve/<int:id>/', views.approve, name='approve'),
    path('applications/decline/<int:id>/', views.decline, name='decline'),
]