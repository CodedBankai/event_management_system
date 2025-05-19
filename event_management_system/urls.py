from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from users import views as users_views  # Make sure this import exists

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('events.urls')),
    path('', include('events.urls')),
    path('', views.home, name='home'),
   # path('accounts/', include('django.contrib.auth.urls')
    # Choose ONE of these approaches for login (not both):
    path('login/', users_views.login_view, name='login'),  # If using custom login view
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
     path('', include('users.urls')),
]

