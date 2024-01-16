from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Order


# class RegUserForm(UserCreationForm):
#     username = forms.CharField(required=True, label = 'username', widget= forms.TextInput(attrs={'placeholder':'Username', 'class': 'form-control'}))
#     email = forms.CharField(required=True, label = 'username', widget= forms.TextInput(attrs={'placeholder':'Username', 'class': 'form-control'}))
#     password = forms.CharField(
#         required=True,
#         label='Password',
#         widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
#     )
    
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2', 'user_type', 'phone')
        
        
# class RegUserForm(UserCreationForm):
#     username = forms.CharField(required=True, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
#     email = forms.EmailField(required=True, label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
#     password1 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1')
        
class RegUserForm(UserCreationForm):
    username = forms.CharField(required=True, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    email = forms.EmailField(required=True, label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password1 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))
    user_type = forms.ChoiceField(required=True,label='User Type',choices=User.USER_TYPE_CHOICES[1:3],widget=forms.Select(attrs={'placeholder': 'Select', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    # def clean_user_type(self):
    #     user_type = self.cleaned_data.get('user_type')
    #     if user_type and user_type.lower() == 'admin':
    #         raise forms.ValidationError("You are not allowed to register as an admin.")
    #     return user_type
        
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label = 'username', widget= forms.TextInput(attrs={'placeholder':'Username', 'class': 'form-control'}))
    password = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
    

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
    