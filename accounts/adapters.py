from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from allauth.core.exceptions import ImmediateHttpResponse
from django.db import IntegrityError

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        user_model = get_user_model()

        if not email:
            messages.error(request, 'Google account does not have an email.')
            raise ImmediateHttpResponse(redirect('login'))

        try:
            user = user_model.objects.get(email=email)
            if not user.is_active:
                messages.error(request, 'Your account is suspended.')
                raise ImmediateHttpResponse(redirect('account_suspended'))

            sociallogin.connect(request, user)
        except user_model.DoesNotExist:
            # Create a new user if one doesn't exist
            user = user_model(email=email)
            base_username = f"{sociallogin.account.extra_data.get('given_name', '')} {sociallogin.account.extra_data.get('family_name', '')}".strip()
            username = base_username
            counter = 1

            while user_model.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            user.username = username
            user.display_name = base_username  # Store the base username without the number
            user.set_unusable_password()
            try:
                user.save()
            except IntegrityError:
                messages.error(request, 'An error occurred while creating your account.')
                raise ImmediateHttpResponse(redirect('login'))

            sociallogin.connect(request, user)

    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        user.set_unusable_password()
        user.save()
        return user