from django.urls import path
from . import views

urlpatterns = [
    path('', views.basic, name='basic'),
    path('home/', views.home, name='home'),
    path('new_search/', views.new_search, name="new_search"),
]