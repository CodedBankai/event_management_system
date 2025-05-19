from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from events.models import Event, Ticket
from django.shortcuts import get_object_or_404

# Add this import at the top of views.py
from .models import Attendee  # or from users.models import Attendee

# Or your custom form if you have one
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Don't log in the user here
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')  # Use the correct URL name
        else:
            # Display form errors to the user
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})






@login_required
def user_dashboard(request):
    # Get all available events
    events = Event.objects.filter(status='Upcoming')
    
    # Get current user's tickets - IMPROVED QUERY
    user_tickets = []
    
    try:
        # Try to get the attendee record first
        attendee = Attendee.objects.get(email=request.user.email)
        
        # If found, get their tickets
        user_tickets = Ticket.objects.filter(attendee=attendee)
        
        # Ensure the attendee is linked to this user
        if not attendee.user:
            attendee.user = request.user
            attendee.save()
    except Attendee.DoesNotExist:
        # No tickets yet
        pass
    search_query = request.GET.get('search', '')
    
    # Use the search query if provided
    if search_query:
        events = events.filter(
            Q(event_name__icontains=search_query) |
            Q(event_type__icontains=search_query) |
            Q(event_description__icontains=search_query)
        )    
    # Rest of your code...
    context = {
        'events': events,
        'user_tickets': user_tickets,
        'search_query': search_query
    }
    
    return render(request, 'user_dashboard.html', context)




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'login.html')


@login_required
def admin_dashboard(request):
    # Security check - only staff users can access
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access the admin dashboard.")
        return redirect('user_dashboard')
    
    # Get all events
    events = Event.objects.all()
    
    # Get all tickets
    tickets = Ticket.objects.all()
    
    # Get all attendees
    attendees = Attendee.objects.all()
    
    context = {
        'events': events,
        'tickets': tickets,
        'attendees': attendees,
        'total_events': events.count(),
        'total_tickets': tickets.count(),
        'total_attendees': attendees.count(),
    }
    
    return render(request, 'admin_dashboard.html', context)
def attendee_detail(request, attendee_id):
    attendee = get_object_or_404(Attendee, attendee_id=attendee_id)
    # Optionally, get tickets for this attendee
    tickets = Ticket.objects.filter(attendee=attendee)
    
    context = {
        'attendee': attendee,
        'tickets': tickets
    }
    
    return render(request, 'attendee_detail.html', context)
