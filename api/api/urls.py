"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from text_analyzer import views as text_analyzer_views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/api/", permanent=False)),
    path("api/users/", include("user_accounts.urls")),
    path("api/text-analyzer/", include("text_analyzer.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # Specific endpoints for text analysis
    path(
        "analyze/",
        text_analyzer_views.TextAnalysisMixins.as_view({"post": "create"}),
        name="text-analyze",
    ),
    path(
        "search/",
        text_analyzer_views.TextAnalysisMixins.as_view({"get": "list"}),
        name="text-search",
    ),
]
