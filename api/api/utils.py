"""
Shared utilities for Django REST Framework
"""

from django.conf import settings
from typing import Union
from rest_framework import routers
from django.contrib.auth.models import User


def get_router() -> Union[routers.DefaultRouter, routers.SimpleRouter]:
    """
    Returns appropriate router based on DEBUG setting.

    - In development (DEBUG=True): DefaultRouter with API root view
    - In production (DEBUG=False): SimpleRouter without API root view

    Usage:
        from api.utils import get_router

        router = get_router()
        router.register(r'users', UserViewSet)
    """
    if settings.DEBUG:
        return routers.DefaultRouter()
    else:
        return routers.SimpleRouter()


def user_is_admin(user: User) -> bool:
    """
    Determine if current user is admin
    """
    if user.is_superuser:
        return True

    return bool(user.is_staff)
