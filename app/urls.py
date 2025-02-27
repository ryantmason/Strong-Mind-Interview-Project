from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .core.views import HomePageView, sign_up, CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('accounts/signup/', sign_up, name='signup'),  # Sign-up view
    path('', HomePageView.as_view(), name='home'),
]
