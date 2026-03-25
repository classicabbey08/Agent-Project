from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/add/', views.property_create, name='property_create'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('properties/<int:pk>/save/', views.save_property, name='save_property'),
    path('agents/', views.agents, name='agents'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]