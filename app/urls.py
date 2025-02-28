from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .core.views import (
    HomePageView,
    ToppingsPageView,
    CustomLoginView,
    sign_up,
    update_topping_status,
    delete_existing_topping,
    add_new_topping,
    update_existing_topping,
    get_available_toppings,
    get_unavailable_toppings,
    get_all_pizzas,
    create_new_pizza,
    delete_existing_pizza,
    update_pizza_details,
    update_pizza_toppings
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('accounts/signup/', sign_up, name='signup'),
    path('', HomePageView.as_view(), name='home'),
    path('available_toppings/', ToppingsPageView.as_view(), name='available_toppings'),
    path('update_topping_status/', update_topping_status, name='update_topping_status'),
    path('delete_existing_topping/', delete_existing_topping, name='delete_existing_topping'),
    path('add_new_topping/', add_new_topping, name='add_new_topping'),
    path('update_existing_topping/', update_existing_topping, name='update_existing_topping'),
    path('get_available_toppings/', get_available_toppings, name='get_available_toppings'),
    path('get_unavailable_toppings/', get_unavailable_toppings, name='get_unavailable_toppings'),
    path('get_all_pizzas/', get_all_pizzas, name='get_all_pizzas'),
    path('create_new_pizza/', create_new_pizza, name='create_new_pizza'),
    path('delete_existing_pizza/', delete_existing_pizza, name='delete_existing_pizza'),
    path('update_pizza_details/', update_pizza_details, name='update_pizza_details'),
    path('update_pizza_toppings/', update_pizza_toppings, name='update_pizza_toppings'),
]
