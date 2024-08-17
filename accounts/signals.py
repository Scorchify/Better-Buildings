from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(pre_social_login)
def pre_social_login_handler(request, sociallogin, **kwargs):
    user = sociallogin.user
    base_username = f"{sociallogin.account.extra_data.get('given_name', '')} {sociallogin.account.extra_data.get('family_name', '')}".strip()
    username = base_username
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    user.username = username
    user.display_name = base_username  # Store the base username without the number
    user.save()