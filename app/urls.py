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
    add_new_topping
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
    path('add_new_topping/', add_new_topping, name='add_new_topping')
]
