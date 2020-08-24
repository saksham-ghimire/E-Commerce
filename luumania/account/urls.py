"""Maccount URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from . import views
from django.conf.urls import url

urlpatterns = [

    path('register/', views.signup , name="signup"),
    path('signup/', views.signup_user , name="signup"),
    path('login/', views.login_view , name='login' ),
    # path('logout', views.logout_view , name='logout'),
    path('logout/', views.logout_view, name='logout'),
    path('update_account/', views.update, name="update"),
    path('user_delete' , views.del_user, name="delete"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),





]
