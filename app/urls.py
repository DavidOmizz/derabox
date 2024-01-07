from django.urls import path
from .views import home, register, test, login, dashboard

urlpatterns = [
    path('', home),
    path('test/', test, name = 'test'),
    path('register/', register , name='register'),
    path('login/', login, name='login'),
    path('dashboard', dashboard, name = 'dashboard'),
]
