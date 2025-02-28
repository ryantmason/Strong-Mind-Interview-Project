import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.views import LoginView
from .models import AvailableToppings, PizzaMasterPieces


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pizza_list'] = PizzaMasterPieces.objects.all()
        return context


class ToppingsPageView(LoginRequiredMixin, TemplateView):
    template_name = "toppings.html"
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_toppings'] = AvailableToppings.objects.all()
        return context


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


def add_new_topping(request):
    """
    Adds a new topping to the available toppings list
    :param request:
    :return: JSON response
    """
    if request.method == 'POST':
        payload = request.POST
        topping_name = payload.get('topping_name')
        available = payload.get('available')

        print("TOPPING NAME: ", topping_name)

        print("AVAILABLE", available)

        try:
            topping = AvailableToppings.objects.create(topping_name=topping_name, available=available)
            topping.save()
            return JsonResponse({'success': True, 'toppingName': topping_name})
        except AvailableToppings.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Topping not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def update_topping_status(request):
    """
    Updates a toppings availability (to account for inventory)
    :param request:
    :return: JSON response
    """
    if request.method == 'POST':
        payload = request.POST
        topping_name = payload.get('topping_name')
        available = payload.get('available') == 'true'
        try:
            topping = AvailableToppings.objects.get(topping_name=topping_name)
            topping.available = available
            topping.save()
            return JsonResponse({'success': True})
        except AvailableToppings.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Topping not found'})
        except Exception as e:
            # Catching any unexpected errors and returning the message
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def delete_existing_topping(request):
    """
    Deletes the selected topping from the list completely
    :param request:
    :return: JSON response
    """
    if request.method == 'POST':
        payload = request.POST
        topping_name = payload.get('topping_name')

        try:
            topping = AvailableToppings.objects.get(topping_name=topping_name)
            topping.delete()
            return JsonResponse({'success': True, 'toppingName': topping_name})
        except AvailableToppings.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Topping not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def update_existing_topping(request):
    if request.method == 'POST':
        payload = request.POST
        topping_name = payload.get('topping_name')

        try:
            topping = AvailableToppings.objects.get(topping_name=topping_name)
            topping.delete()
            return JsonResponse({'success': True, 'toppingName': topping_name})
        except AvailableToppings.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Topping not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def create_new_pizza(request):
    pass


def update_existing_pizza_details():
    pass


def delete_existing_pizza(request):
    pass


def update_existing_pizza_toppings(request):
    pass
