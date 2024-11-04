from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'accounts'

urlpatterns = [
   path('', views.dashboard, name='dashboard'),
   path('register/', views.register, name='register'),
   path('login/', views.login_view, name='login'),
   path('logout/', views.my_logout, name='logout'),
   path('profile_edit/', views.profile_edit, name='profile_edit'),
   path('password_change/', views.PasswordChangeView.as_view(success_url = '/'), name='password_change'),
   path('notifications_/', views.notifications_, name='notifications_'),


]