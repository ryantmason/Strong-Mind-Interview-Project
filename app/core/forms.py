from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# Django's built-in form system for authentication (login/logout)
class SignUpForm(UserCreationForm):
    USER_GROUPS = (
        ('chef', 'Pizza Chef'),
        ('owner', 'Pizza Store Owner'),
    )

    # for simplicity allow users to select their own user group
    user_group = forms.ChoiceField(choices=USER_GROUPS, label='Select User Group')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
