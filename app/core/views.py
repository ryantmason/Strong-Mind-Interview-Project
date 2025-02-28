import json

# Django core imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

# Local app imports
from .forms import SignUpForm
from .models import AvailableToppings, PizzaMasterPieces
from .decorators import group_required



class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pizza_list'] = PizzaMasterPieces.objects.all()
        return context


# Ensures user is redirected directly to home page instead of Djangos default profile url
class CustomLoginView(LoginView):
    def get_redirect_url(self):
        return super().get_redirect_url() or '/'


@method_decorator(group_required(['Pizza Store Owner']), name='dispatch')
class ToppingsPageView(LoginRequiredMixin, TemplateView):
    template_name = "toppings.html"
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_toppings'] = AvailableToppings.objects.all()
        return context


@csrf_protect
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


# --------------------
# Toppings Related Methods
# --------------------

@group_required(['Pizza Store Owner'])
def add_new_topping(request):
    """
    Adds a new topping to the available toppings list
    :param request:
    :return: JSON response
    """
    if request.method == 'POST':
        payload = request.POST
        topping_name = payload.get('topping_name').title()
        available = payload.get('available')

        try:
            topping = AvailableToppings.objects.create(topping_name=topping_name, available=available)
            topping.save()
            return JsonResponse({'success': True, 'toppingName': topping_name})
        except AvailableToppings.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Topping not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@group_required(['Pizza Store Owner'])
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


@group_required(['Pizza Store Owner'])
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


@group_required(['Pizza Store Owner'])
def update_existing_topping(request):
    """
    Updates the selected topping
    :param request:
    :return: JSON response
    """
    if request.method == 'POST':
        payload = request.POST
        original_topping_name = payload.get('original_topping_name')
        new_topping_name = payload.get('new_topping_name').title()
        new_availability = payload.get('new_availability')

        try:
            topping = AvailableToppings.objects.get(topping_name=original_topping_name)
            topping.topping_name = new_topping_name
            topping.available = new_availability
            topping.save()
            return JsonResponse({'success': True, 'toppingName': new_topping_name})
        except AvailableToppings.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Topping not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@group_required(['Pizza Store Owner', 'Pizza Chef'])
def get_available_toppings(request):
    """
    Returns toppings marked as available
    :param request:
    :return: JSON response
    """
    toppings = AvailableToppings.objects.filter(available=True)  # Fetch all available toppings
    toppings_list = [{'topping_name': topping.topping_name} for topping in toppings]  # Prepare the data

    print("Toppings list ", toppings_list)

    return JsonResponse({'success': True, 'toppings': toppings_list})


@group_required(['Pizza Store Owner', 'Pizza Chef'])
def get_unavailable_toppings(request):
    """
    Returns toppings marked as unavailable
    :param request:
    :return: JSON response
    """
    toppings = AvailableToppings.objects.filter(available=False)  # Fetch all available toppings
    toppings_list = [{'topping_name': topping.topping_name} for topping in toppings]  # Prepare the data

    return JsonResponse({'success': True, 'toppings': toppings_list})


# --------------------
# Pizza Related Methods
# --------------------
@group_required(['Pizza Store Owner', 'Pizza Chef'])
def get_all_pizzas(request):
    """
    Returns a list of all existing pizzas
    :param request:
    :return: JSON response
    """
    pizzas = PizzaMasterPieces.objects.all()
    pizza_list = []

    for pizza in pizzas:
        toppings = [topping.topping_name for topping in pizza.toppings.all()]
        pizza_list.append({
            'pizzaName': pizza.pizza_name,
            'toppings': toppings,
        })

    return JsonResponse({'success': True, 'pizzas': pizza_list})


@group_required(['Pizza Store Owner', 'Pizza Chef'])
def create_new_pizza(request):
    """
    Creates a new pizza object in the database
    :param request:
    :return: JSON response
    """
    if request.method == 'POST':
        pizza_name = request.POST.get('pizza-name').title()
        selected_toppings = request.POST.getlist('topping-list')  # Get list of selected toppings

        if not pizza_name or not selected_toppings:
            return JsonResponse({'success': False, 'error': 'Pizza name and toppings are required'})

        try:
            existing_pizza = PizzaMasterPieces.objects.filter(
                toppings__topping_name__in=selected_toppings
            ).annotate(num_toppings=Count('toppings')).filter(num_toppings=len(selected_toppings)).first()

            if existing_pizza:
                return JsonResponse({
                    'success': False,
                    'error': f'A pizza with the same toppings already exists: {existing_pizza.pizza_name}'
                })

            pizza = PizzaMasterPieces.objects.create(pizza_name=pizza_name)

            toppings = AvailableToppings.objects.filter(topping_name__in=selected_toppings, available=True)
            pizza.toppings.set(toppings)

            toppings_names = [topping.topping_name for topping in toppings]

            return JsonResponse({
                'success': True,
                'pizza_name': pizza_name,
                'toppings': toppings_names
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@group_required(['Pizza Store Owner', 'Pizza Chef'])
def delete_existing_pizza(request):
    """
        Deletes the selected Pizza from the database
        :param request:
        :return: JSON response
        """
    if request.method == 'POST':
        payload = request.POST
        pizza_name = payload.get('pizza_name')

        try:
            pizza = PizzaMasterPieces.objects.get(pizza_name=pizza_name)
            pizza.delete()
            return JsonResponse({'success': True, 'pizzaName': pizza_name})
        except PizzaMasterPieces.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Topping not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@group_required(['Pizza Store Owner', 'Pizza Chef'])
def update_pizza_details(request):
    """
    Updates the details of the selected Pizza from the database
    :param request:
    :return: JSON response
    """
    if request.method == 'POST':
        original_pizza_name = request.POST.get('original_pizza_name')
        new_pizza_name = request.POST.get('new_pizza_name').title()
        try:
            pizza = PizzaMasterPieces.objects.get(pizza_name=original_pizza_name)
            pizza.pizza_name = new_pizza_name
            pizza.save()
            return JsonResponse({'success': True, 'newPizzaName': new_pizza_name})
        except PizzaMasterPieces.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Pizza not found'})


@group_required(['Pizza Store Owner', 'Pizza Chef'])
def update_pizza_toppings(request):
    """
    Updates the toppings of the desired Pizza
    :param request:
    :return: JSONResponse
    """
    if request.method == 'POST':
        pizza_name = request.POST.get('pizza_name')
        topping_list = json.loads(request.POST.get('topping_list'))  # Parse the JSON string into a Python list

        try:
            existing_pizza = PizzaMasterPieces.objects.filter(
                toppings__topping_name__in=topping_list
            ).annotate(num_toppings=Count('toppings')).filter(num_toppings=len(topping_list)).first()

            if existing_pizza:
                return JsonResponse({
                    'success': False,
                    'error': f'A pizza with the same toppings already exists: {existing_pizza.pizza_name}'
                })

            pizza = PizzaMasterPieces.objects.get(pizza_name=pizza_name)
            # Clear existing toppings
            pizza.toppings.clear()

            # Add selected toppings
            for topping_name in topping_list:
                topping = AvailableToppings.objects.get(topping_name=topping_name)
                pizza.toppings.add(topping)

            return JsonResponse({'success': True, 'message': 'Toppings updated successfully'})
        except PizzaMasterPieces.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Pizza not found'})
        except AvailableToppings.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'One or more toppings not found'})
