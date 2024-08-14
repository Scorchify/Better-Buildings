from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email not in ['171524@mcpsmd.net', 'aydenzyeung@gmail.com'] and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(required=False)

    def confirm_login_allowed(self, user):
        if user.is_suspended:
            raise forms.ValidationError(
                "This account is suspended.",
                code='inactive',
            )
class CompleteSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2")