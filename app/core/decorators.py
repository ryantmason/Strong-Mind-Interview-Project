from django.http import HttpResponseRedirect
from django.urls import reverse
from functools import wraps


def group_required(group_list):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('accounts/signup/'))
            user_groups = request.user.groups.values_list('name', flat=True)
            print("GROUPS", user_groups)
            if not any(group in group_list for group in user_groups):
                return HttpResponseRedirect(reverse('home'))
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
