from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),  # Fixed double slash
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register-event//', views.register_event, name='register_event'),
    path('register-event/<int:event_id>/', views.register_event, name='register_event'),
    path('create-event/', views.create_event, name='create_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),  # Fixed incorrect format
    # Add this line to your urlpatterns list
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
   # Add this line to your urlpatterns list
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),

]

