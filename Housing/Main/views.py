from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def property_list(request):
    return render(request, 'property_list.html', {})

def property_create(request):
    return render(request, 'property_create.html', {})

def dashboard(request):
    return render(request, 'dashboard.html', {})

def agent_dashboard(request):
    return render(request, 'agent_dashboard.html', {})

def login(request):
    return render(request, 'login.html', {})

def signup(request):
    return render(request, 'signup.html', {})