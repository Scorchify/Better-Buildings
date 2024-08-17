from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

@receiver(pre_social_login)
def pre_social_login_handler(request, sociallogin, **kwargs):
    user = sociallogin.user

    # Fetch username and password from the session
    username = request.session.get('signup_username')
    password = request.session.get('signup_password')

    if username:
        user.username = username
    if password:
        user.set_password(password)
    
    # Ensure the email from the social account is saved
    user.email = sociallogin.account.extra_data.get('email', '')

    user.save()