"""ShoppingList URL Configuration

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
from django.urls import path

from shopping import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='main_url'),
    path('users/<int:id>/', views.person_page_view, name='user_page_url'),
    path('users/register', views.register_person_view, name='register_person_view'),
    path('users/save', views.save_person_view, name='save_person_view'),
]
