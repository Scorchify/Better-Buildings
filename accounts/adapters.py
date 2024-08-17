from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from allauth.core.exceptions import ImmediateHttpResponse
from .forms import CustomSocialSignupForm
from django.conf import settings

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        user_model = get_user_model()

        if not email:
            messages.error(request, 'Google account does not have an email.')
            raise ImmediateHttpResponse(redirect('register'))

        try:
            user = user_model.objects.get(email=email)
            if not user.username or not user.has_usable_password():
                messages.error(request, 'No account associated with this Google email. Please register first.')
                raise ImmediateHttpResponse(redirect('register'))

            if not user.is_active:
                messages.error(request, 'Your account is suspended.')
                raise ImmediateHttpResponse(redirect('account_suspended'))

            sociallogin.connect(request, user)
        except user_model.DoesNotExist:
            messages.error(request, 'No account associated with this Google email. Please register first.')
            raise ImmediateHttpResponse(redirect('register'))

    def save_user(self, request, sociallogin, form=None):
        # Only save the user if the form is complete and valid
        if form and isinstance(form, CustomSocialSignupForm):
            user = super().save_user(request, sociallogin, form=form)
            user.set_password(form.cleaned_data["password1"])
            user.save()
        else:
            # Prevent account creation if form is not valid
            return None

        return super().save_user(request, sociallogin, form=form)
