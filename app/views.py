from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomerProfile, DeliveryPersonProfile
from .forms import RegUserForm, LoginForm, CreateOrderForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required



# Create your views here.

def home(request):
    return render(request, 'index.html', )

def test(request):
    return render(request, 'test.html')
@login_required
def orderForm(request):
    if request.method == 'POST':
        order_form = CreateOrderForm(request.POST)
        if order_form.is_valid():
            order_form.save()
            # user = order_form.cleaned_data.get('username','email')
    return render(request, 'dashboard/create-order-form.html')
@login_required
def orderItems(request):
    return render(request, 'dashboard/order-items-form.html')
@login_required
def orderHistory(request):
    return render(request, 'dashboard/order-history-form.html')

# def dashboard(request):
#     return render(request, 'dashboard/index.html')

@login_required
def dashboard(request):
    customersProfile = CustomerProfile.objects.all()
    deliveryProfile = DeliveryPersonProfile.objects.all()
    user_type = request.user.user_type
    users = request.user
    customersprofile = users
    deliveryprofile = users
    context = {
        'user_type': user_type,
        'user': request.user.username,
        'customersprofile': customersprofile,
        'deliveryprofile': deliveryprofile
    }
    # print(customerProfile)
    return render(request, 'dashboard/index.html', context)


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
            messages.warning(request, 'Username Or password is incorrect')

    else:
        form = LoginForm()

    return render(request, 'dashboard/signin.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
# def loginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             auth_login(request, user)
#             return redirect('dashboard')
#         else:
#             print('Invalid login failed')
#             messages.warning(request, 'Username Or password is incorrect')
    
#     context = {}      
#     return render(request, 'dashboard/signin.html', context)
