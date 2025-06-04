from django.urls import path
from . import views, homepage,about,contact

urlpatterns = [
    path('', views.homePage, name='homepage'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]