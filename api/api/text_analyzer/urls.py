from django.urls import path, include
from api.utils import get_router
from . import views

router = get_router()
router.register(r"text-analyses", views.TextAnalysisMixins)

urlpatterns = [
    path("", include(router.urls)),
]
