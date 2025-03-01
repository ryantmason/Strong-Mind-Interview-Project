from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms


# Django's built-in form system for authentication (login/logout)
class SignUpForm(UserCreationForm):
    # Dynamically fetch all groups from the database
    user_group = forms.ModelChoiceField(queryset=Group.objects.all(), label='Select User Group')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'user_group']

    def save(self, commit=True):
        # Save the user instance
        user = super().save(commit=False)

        if commit:
            user.save()

        # Get the selected user group
        selected_group = self.cleaned_data['user_group']

        # Assign the user to the corresponding group
        user.groups.add(selected_group)

        return user
