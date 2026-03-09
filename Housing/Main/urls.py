from django.urls import path
from .views import home, property_list,property_create,dashboard,agent_dashboard,login,signup

urlpatterns = [
    path('', home, name='home'),                       
    path('properties/', property_list, name='property_list'),
    path('add-property/', property_create, name='property_create'),
    path('dashboard/', dashboard, name='dashboard'),
    path('agent-dashboard/', agent_dashboard, name='agent_dashboard'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
]