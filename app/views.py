from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomerProfile, DeliveryPersonProfile
from .forms import RegUserForm, LoginForm

# Create your views here.

def home(request):
    return render(request, 'index.html', )

def test(request):
    return render(request, 'test.html')

# def dashboard(request):
#     return render(request, 'dashboard/index.html')

def dashboard(request):
    user_type = request.user.user_type
    return render(request, 'dashboard/index.html', {'user_type': user_type, 'user': request.user.username})


def register(request):
    if request.method == 'POST':
        form = RegUserForm(request.POST)
        if form.is_valid():
            # user_type = form.cleaned_data.get('user_type', 'customer')
            user_type = form.cleaned_data['user_type']
            user = form.save()

            if user_type == 'customer':
                CustomerProfile.objects.create(user=user)
            elif user_type == 'delivery':
                DeliveryPersonProfile.objects.create(user=user)

            # Redirect to the appropriate page after registration
            return redirect('login')
    else:
        form = RegUserForm()

    return render(request, 'dashboard/signup.html', {'form': form, 'user': form.instance})

from django.contrib.auth import login as auth_login


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # # Redirect to the appropriate page after login
            return redirect('dashboard')  # Adjust the redirect URL as needed

    else:
        form = LoginForm()

    return render(request, 'dashboard/signin.html', {'form': form})
