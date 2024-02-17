from django.shortcuts import render

from .forms import LoginForm, UserRegistrationForm


def getLogin(request):
    login_form = LoginForm()
    return {'login_form': login_form}


def userRegister(request):
    user_form = UserRegistrationForm()
    return {'user_form': user_form}
