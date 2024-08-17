from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            # Try to fetch the user by searching the username field
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # If no user is found, try to fetch the user by email
            try:
                user = UserModel._default_manager.get(email=username)
            except UserModel.DoesNotExist:
                # If no user is found with the email, return None
                return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user