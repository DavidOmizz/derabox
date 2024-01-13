from django.urls import path
from .views import home, register, test, login, dashboard, orderForm, orderItems, orderHistory

urlpatterns = [
    path('', home),
    path('test/', test, name = 'test'),
    path('register/', register , name='register'),
    path('login/', login, name='login'),
    path('dashboard', dashboard, name = 'dashboard'),
    path('creation-order', orderForm, name = 'creation-order'),
    path('creation-order', orderForm, name = 'creation-order'),
    path('order-items', orderItems, name = 'order-items'),
    path('order-history', orderHistory, name = 'order-history'),
]
