import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.views import LoginView


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = '/accounts/login/'


# Ensures user is redirected directly to home page instead of Djangos default profile url
class CustomLoginView(LoginView):
    def get_redirect_url(self):
        return super().get_redirect_url() or '/'


@csrf_protect
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})
