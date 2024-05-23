from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomerProfile, DeliveryPersonProfile, Order, OrderHistory
from .forms import RegUserForm, LoginForm, CreateOrderForm, CreateOrderItemForm, UpdateOrderForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView, ListView,DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


# Create your views here.

def home(request):
    return render(request, 'index.html', )

def test(request):
    return render(request, 'test.html')

@login_required
def orderForm(request):
    # order_form = CreateOrderForm()
    if request.method == 'POST':
        order_form = CreateOrderForm(request.POST)
        if order_form.is_valid():
            new_order = order_form.save()
            # form.save()
            # Assuming you want to use the order ID in the subsequent views or sessions
            request.session['new_order_id'] = new_order.pk
            return redirect('order-items')
        else:
            print(order_form.errors)
    else:
        print('An error occurred while creating order')
        order_form = CreateOrderForm()
            # user = order_form.cleaned_data.get('username','email')
    return render(request, 'dashboard/create-order-form.html', {'orderForm': order_form})

# class AddPost(SuccessMessageMixin, CreateView):
#     model = 
#     template_name = 'cbv_form.html'
#     form_class = FormDetails
#     success_url = reverse_lazy('app:add_post')
#     success_message = 'Updated successfully'

# @login_required
# def orderItems(request):
#     order_item_form =  CreateOderItemForm()
#     if request.method == 'POST':
#         order_item_form = CreateOderItemForm(request.POST)
#         if order_item_form.is_valid():
#             order_item_form.save()
#             return redirect('order-history')
#         else: 
#             print('This is not a valid order item')
#     else:
#         # print('An error occurred')
#         order_item_form = CreateOderItemForm()
#     return render(request, 'dashboard/order-items-form.html', {'orderItems': order_item_form})


# def orderItems(request):
#     if request.method == 'POST':
#         order_item_form = CreateOrderItemForm(request.POST)
#         if order_item_form.is_valid():
#             # Save the order item with the associated order
#             order_item = order_item_form.save(commit=False)
#             order_item.order = Order.objects.get(pk=request.session.get('new_order_id'))
#             order_item.save()
#             # return redirect('order-history')
#             print(order_item.order)
#         else: 
#             print('This is not a valid order item')
#     else:
#         # Pass the new order instance to the order item form as initial data
#         order_item_form = CreateOrderItemForm(initial={'order': Order.objects.get(pk=request.session.get('new_order_id'))})
#     return render(request, 'dashboard/order-items-form.html', {'orderItems': order_item_form})


def orderItems(request):
    if request.method == 'POST':
        order_item_form = CreateOrderItemForm(request.POST)
        if order_item_form.is_valid():
            try:
                order = get_object_or_404(Order, pk=request.session.get('new_order_id'))
                order_item = order_item_form.save(commit=False)
                order_item.order = order
                order_item.save()
                # return redirect('order-history')
                print(order_item.order)
                return redirect('order-history')
            except KeyError:
                print('Order ID not found in session')
            except Order.DoesNotExist:
                print('Order not found')
        else:
            print('This is not a valid order item')
    else:
        # Handle cases where the order might not exist or no ID is in session
        try:
            initial_order = get_object_or_404(Order, pk=request.session.get('new_order_id'))
            order_item_form = CreateOrderItemForm(initial={'order': initial_order})
        except KeyError:
            print('Order ID not found in session')
            order_item_form = CreateOrderItemForm()
        except Order.DoesNotExist:
            print('Order not found')
            order_item_form = CreateOrderItemForm()

    return render(request, 'dashboard/order-items-form.html', {'orderItems': order_item_form})

@login_required
def orderHistory(request):
    # orders = OrderHistory.objects.all().order_by('-timestamp')
    # orders = Order.objects.all().order_by('-created_at')
    orders = Order.objects.prefetch_related('items').order_by('-created_at')
    # orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'dashboard/order-history-form.html', context)

class MyOrderHistory(ListView):
    model = Order
    template_name = 'dashboard/order-history-form.html'
    context_object_name = 'orders'
    

    def get_queryset(self):
        # Order the results by 'created_at' in descending order
        return Order.objects.all().order_by('created_at')

# class UpdateOrder(UpdateView):
#     model = OrderHistory
#     template_name = 'dashboard/update-order.html'
#     form_class = CreateOrderForm
#     fields = [ 
#         "order", 
#         "status"
#     ] 
#     # context_object_name = 'update-order'
#     success_url = reverse_lazy('order-history')
    
class UpdateOrder(UpdateView):
    model = Order
    template_name = 'dashboard/update-order.html'
    form_class = UpdateOrderForm
    success_url = reverse_lazy('order-history')

    def get_initial(self):
        initial = super().get_initial()
        order_instance = self.get_object()  # Get the instance of Order
        initial['user'] = order_instance.user
        initial['product_name'] = order_instance.product_name
        initial['status'] = order_instance.status
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        order_items = order.items.all()  # Retrieve associated order items
        context['order_items'] = order_items
        return context


class SingleOrder(DetailView):
    model = Order
    template_name = 'dashboard/single-order.html'
    context_object_name = 'order_detail'
    

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
