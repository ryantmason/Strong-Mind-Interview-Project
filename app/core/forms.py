from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Django's built-in form system for authentication (login/logout)
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
