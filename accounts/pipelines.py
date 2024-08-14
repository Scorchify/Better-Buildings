from django.shortcuts import redirect

def redirect_to_complete_signup(strategy, details, user=None, *args, **kwargs):
    if user is None:
        return redirect('complete_signup')  # Redirect to your complete_signup URL