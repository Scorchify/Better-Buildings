from django import forms
from django.contrib.auth.forms import AuthenticationForm
from allauth.account.forms import SignupForm

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.is_suspended:
            raise forms.ValidationError(
                "This account is suspended.",
                code='inactive',
            )