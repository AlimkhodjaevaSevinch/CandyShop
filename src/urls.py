"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from shop.views import categories_list, candies_list, add_to_cart, get_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', categories_list, name='home'),
    path('create_order/', get_cart, name='create_order'),
    path('cart/', get_cart, name='cart'),
    path('add_to_cart/<int:candy_id>/', add_to_cart, name='add_to_cart'),
    path('category/<slug:category_slug>/', candies_list, name='candies_list'),
    path('users/', include('users.urls')),
]
