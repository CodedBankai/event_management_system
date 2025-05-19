from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# At the top of your users/urls.py file, add:
from events import views as admi  # Or whatever app contains the admin dashboard view

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    # In your main project urls.py
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

