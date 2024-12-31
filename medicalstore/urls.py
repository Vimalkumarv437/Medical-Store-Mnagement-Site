"""
URL configuration for medicalstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from medicalapp import views
urlpatterns = [
    
    path('',views.signup_page,name='signup'),
    path('login',views.login_page,name='login_page'),
    path('home',views.home_page,name='home'),
    path('add',views.add_medicine,name='add_medicine'),
    path('list ',views.list_medicines,name='list_medicines'),
    path('edit/<int:medicine_id>/',views.edit_medicine, name='edit_medicine'),
    path('delete/<int:medicine_id>/',views.delete_medicine,name='delete_medicine'),
    path('logout/',views.logout_view, name='logout'),
    path('contactus',views. contact_us, name='contactus')
   
]

