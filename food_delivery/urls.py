"""
URL configuration for food_delivery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from products.views import home
from food_delivery import admin_security  # Configures the shared admin site.

urlpatterns = [

    path(
        settings.ADMIN_URL,
        admin.site.urls
    ),
    path("", include("django.contrib.auth.urls")),
    path("", home, name="home"),        #FOR BOTH USER & ADMIN
    path(
        "customers/",
        include("customers.urls")
    ),

    path(
        "",
        include("products.urls")        #FOR ONLY ADMIN
    ),

    path(
        "orders/",
        include("orders.urls")
    ),
]

# django.conf.urls.static.static() is a no-op when DEBUG is False, which is
# the project default. Serve uploaded media explicitly so product and
# restaurant images load under runserver without a DEBUG=True environment.
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]
