from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from account.forms import UserEditForm, LoginForm, UserRegistrationForm
from account.models import Customer


def register_customer(request):
    register_form = UserRegistrationForm()
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            new_user = Customer.objects.create_user(
                username=register_form.cleaned_data["username"],
                first_name=register_form.cleaned_data["first_name"],
                last_name=register_form.cleaned_data["last_name"],
                email=register_form.cleaned_data["email"],
                password= register_form.cleaned_data["password"],
            )
            new_user.save()
            login(request, new_user)  # Log in the user
            return redirect('myshop:home')
    else:
        return render(request, 'registration/login.html', {
            'register_form': register_form
        })


def login_customer(request):
    register_form = UserRegistrationForm()
    user_form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(f'user is : {user}')
            if user is not None:
                login(request, user)
                return redirect('myshop:home')  # Redirect to dashboard upon successful login
    else:
        user_form = LoginForm()
    return render(request, 'registration/login.html', {'user_form': user_form, 'register_form': register_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form})


@login_required
def dashboard(request):
    # Logic to retrieve user data or any other dashboard-related data
    # For example:
    user = request.user
    user_data = {
        'username': user.username,
        'email': user.email,
        # Add more user-related data as needed
    }

    return render(request, 'account/dashboard.html', {'user_data': user_data})
