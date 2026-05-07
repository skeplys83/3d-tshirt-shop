"""
URL configuration for shopcore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

version = 'v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/{version}/auth/', include('users.urls')),
    path(f'api/{version}/products/', include('products.urls')),
    path(f'api/{version}/orders/', include('orders.urls')),
    path(f'api/{version}/payments/', include('payment.urls')),
    path(f'api/{version}/email/', include('email_service.urls')),
]
