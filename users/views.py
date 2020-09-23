from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.models import User

# Create your views here.

def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Welcome {username}, Your account is created')
            return redirect('loginurl')
    else:
        form = RegisterForm()
    return render (request, 'users/register.html', {"form" : form})

def logout_view(request):
    logout(request)    
    return redirect('loginurl')
  
