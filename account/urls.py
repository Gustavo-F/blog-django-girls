from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('forgot/', views.ForgotPassword.as_view(), name='forgot'),

    path(
        'passwordreset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='account/reset_password.html'),
        name='password_reset'
    ),

    path(
        'passwordreset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='account/reset_password_complete.html'),
        name='password_reset_complete'
    ),
]
