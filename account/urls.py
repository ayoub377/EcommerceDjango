from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [

    path('login/', views.login_customer, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register_customer, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/', views.edit, name='edit'),

]
