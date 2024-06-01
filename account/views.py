from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# Create your views here.
from account.forms import UserEditForm, LoginForm, UserRegistrationForm
from account.models import Customer
from myshop.forms import ReviewForm
from myshop.models import Review
from orders.models import Order


def register_customer(request):
    register_form = UserRegistrationForm()
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        next_url = request.POST.get('next', '/')
        if register_form.is_valid():
            new_user = Customer.objects.create_user(
                username=register_form.cleaned_data["username"],
                first_name=register_form.cleaned_data["first_name"],
                last_name=register_form.cleaned_data["last_name"],
                email=register_form.cleaned_data["email"],
                password=register_form.cleaned_data["password"],
            )
            new_user.save()
            login(request, new_user)  # Log in the user
            return redirect(next_url)
    else:
        return render(request, 'registration/login.html', {
            'register_form': register_form
        })


def login_customer(request):
    register_form = UserRegistrationForm()
    user_form = LoginForm()
    if request.method == 'POST':
        next_url = request.POST.get('next','/')
        if next_url=='':
            next_url='home'
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)  # Redirect to dashboard upon successful login
    else:
        user_form = LoginForm()
    return render(request, 'registration/login.html', {'user_form': user_form, 'register_form': register_form})


@login_required
def dashboard(request):
    # Logic to retrieve user data or any other dashboard-related data
    user = request.user
    user_data = {
        'username': user.username,
        'email': user.email,
        # Add more user-related data as needed
    }

    # Fetch customer and orders
    customer = Customer.objects.get(username=user.username)
    orders = Order.objects.filter(customer=customer)
    reviews = Review.objects.filter(user=user)
    user_form = UserEditForm(instance=user)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = user
            review.save()
            return redirect('account:dashboard')  # Redirect to the dashboard to show the form again
    else:
        review_form = ReviewForm()

    context = {
        'user_data': user_data,
        'orders': orders,
        'review_form': review_form,
        'reviews': reviews,
        'user_form': user_form
    }

    return render(request, 'account/dashboard.html', context)


@login_required
def edit_account(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        if user_form.is_valid():
            update_user = user_form.save(commit=False)
            new_password = user_form.cleaned_data.get('new_password')

            if new_password:
                update_user.set_password(new_password)
                update_user.save()
            # You may want to add a success message or redirect after saving
            return redirect('account:dashboard')  # Change to your success URL
        else:
            return render(request, 'account/dashboard.html', {'user_form':user_form},status=400)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account:dashboard'))
    else:
        form = ReviewForm(instance=review)


    return render(request, 'account/edit_reviews.html', {
        'form_reviews': form,
        'review': review,
    })
