from django.urls import path, include
from api.utils import get_router
from . import views

router = get_router()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.UserViewSet.as_view({"post": "create"}), name="register"),
]
