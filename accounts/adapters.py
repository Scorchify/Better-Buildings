from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from .forms import CustomSocialSignupForm

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        User = get_user_model()
        username = slugify(user.username)
        unique_username = username
        counter = 1

        while User.objects.filter(username=unique_username).exists():
            unique_username = f"{username}-{counter}"
            counter += 1

        user.username = unique_username
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        if isinstance(form, CustomSocialSignupForm):
            user.set_password(form.cleaned_data["password1"])
            user.save()
        return user