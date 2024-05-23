from django.urls import path
from .views import home, register, test, login, dashboard, orderForm, orderItems, orderHistory, logout_view, UpdateOrder, SingleOrder, MyOrderHistory
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home),
    path('test/', test, name = 'test'),
    path('register/', register , name='register'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('logout', auth_views.LogoutView.as_view(template_name= 'dashboard/logout.html'), name = 'logout'),
    path('dashboard', dashboard, name = 'dashboard'),
    # path('creation-order', orderForm, name = 'creation-order'),
    path('creation-order', orderForm, name = 'creation-order'),
    path('order-items', orderItems, name = 'order-items'),
    path('order-history', orderHistory, name = 'order-history'),
    # path('order-history', MyOrderHistory.as_view(), name='order-history'),
    path('update-order/<int:pk>', UpdateOrder.as_view(),name='update-order'),
    path('order-detail/<int:pk>', SingleOrder.as_view(),name='order-detail'),
]
