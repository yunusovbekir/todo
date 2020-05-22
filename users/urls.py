from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_views

USER_URLS = [
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.ProfileView.as_view(), name='profile'),
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name='logout'),
]

PASSWORD_URLS = [
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password-reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password-reset-done.html'),
         name='password_reset_done'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password-reset-complete.html'),
         name='password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password-reset-confirm.html'),
         name='password_reset_confirm'),
]

urlpatterns = USER_URLS + PASSWORD_URLS
