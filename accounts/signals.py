from allauth.socialaccount.signals import pre_social_login
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

@receiver(pre_social_login)
def pre_social_login_handler(request, sociallogin, **kwargs):
    user = sociallogin.user
    base_username = f"{sociallogin.account.extra_data.get('given_name', '')} {sociallogin.account.extra_data.get('family_name', '')}".strip()
    username = base_username
    counter = 0
    
    # Start with counter 0 and keep incrementing it until a unique username is found
    while User.objects.filter(username=username).exists():
        counter += 1
        username = f"{base_username}{counter}" if counter > 0 else base_username
    
    user.username = username
    user.display_name = base_username  # Store the base username without the number
    user.save()

    # Add the user to the "student" group
    student_group, created = Group.objects.get_or_create(name='student')
    user.groups.add(student_group)

@receiver(post_save, sender=User)
def add_user_to_student_group(sender, instance, created, **kwargs):
    if created:
        student_group, created = Group.objects.get_or_create(name='student')
        instance.groups.add(student_group)