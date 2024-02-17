from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from account.models import Customer


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput(attrs={
                                'class': 'form-input form-wide',
                                'name': 'email'
                            }))

    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-input form-wide',
                                   'data-toggle': 'password', 'id': 'password',
                                   'name': 'password',
                               }))


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=50,
                                 required=True,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-input form-wide',
                                     'name': 'first_name',
                                 }))
    last_name = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-input form-wide',
                                    'name': 'last_name',
                                }))
    email = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.EmailInput(attrs={
                                'class': 'form-input form-wide',
                                'name': 'email'
                            }))

    username = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput(attrs={
                                'class': 'form-input form-wide',
                                'name': 'username'
                            }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-input form-wide',
                                   'data-toggle': 'password',
                                   'name': 'password2',
                               }))

    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-input form-wide',
                                    'data-toggle': 'password',
                                    'name': 'password2',
                                }))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
