from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from allauth.account.forms import SignupForm

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.is_suspended:
            raise forms.ValidationError(
                "This account is suspended.",
                code='inactive',
            )

class CustomSocialSignupForm(SignupForm):
    class Media:
        css = {
            'all': ('css/accounts.css',)
        }
        
    username = forms.CharField(
        label='Username', 
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'accounts-field'})
    )
    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={'class': 'accounts-field'}), 
        required=True
    )
    password2 = forms.CharField(
        label='Password (again)', 
        widget=forms.PasswordInput(attrs={'class': 'accounts-field'}), 
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            del self.fields['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, request):
        user = super().save(request)
        user.username = self.cleaned_data["username"]
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user
    