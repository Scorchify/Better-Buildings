from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),  # Keeps the auth URLs under the accounts namespace
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('suspend/<int:user_id>/', views.suspend_user, name='suspend_user'),
    path('unsuspend/<int:user_id>/', views.unsuspend_user, name='unsuspend_user'),
    path('profile/', views.profile, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('suspended_users/', views.suspended_users, name='suspended_users'),
    path('account_suspended/', views.account_suspended, name='account_suspended'),
]
