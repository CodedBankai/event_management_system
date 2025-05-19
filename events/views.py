from django.shortcuts import render
from .models import Event, Ticket, Attendee
from django.shortcuts import render
from .models import Event
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from users.models import Attendee  # Assuming Attendee is in your users app


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


def admin_dashboard(request):
    if not request.user.is_staff:  # Ensure only admin users can access this view
        return render(request, '403.html')  # Render a "403 Forbidden" page if not admin
    
    events = Event.objects.all()
    tickets = Ticket.objects.select_related('event', 'attendee')
    attendees = Attendee.objects.all()
    
    context = {
        'events': events,
        'tickets': tickets,
        'attendees': attendees,
    }
    return render(request, 'admin_dashboard.html', context)

def user_dashboard(request):
    if request.user.is_staff:  # Prevent admin users from accessing this view
        return render(request, '403.html')  # Render a "403 Forbidden" page if admin
    
    events = Event.objects.all()  # Fetch all events for browsing
    context = {
        'events': events,
    }
    return render(request, 'user_dashboard.html', context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    return render(request, 'event_detail.html', {'event': event})


# If your Attendee model is in a different app, adjust the import

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    # Define ticket options
    ticket_options = [
        {'type': 'Standard', 'price': 49.99},
        {'type': 'Premium', 'price': 99.99},
        {'type': 'VIP', 'price': 149.99}
    ]
    if request.method == 'POST':
        ticket_type = request.POST.get('ticket_type')
        
        # Find the price for this ticket type
        price = 0
        for option in ticket_options:
            if option['type'] == ticket_type:
                price = option['price']
                break
        
        # IMPROVED: Get or create attendee record with explicit user link
        try:
            attendee = Attendee.objects.get(email=request.user.email)
            # Update user link if missing
            if not attendee.user:
                attendee.user = request.user
                attendee.save()
        except Attendee.DoesNotExist:
            # Create new attendee
            attendee = Attendee.objects.create(
                user=request.user,
                email=request.user.email,
                first_name=request.user.first_name or request.user.username,
                last_name=request.user.last_name or ''
            )
        
        # Create the ticket
        ticket = Ticket.objects.create(
            event=event,
            attendee=attendee,
            ticket_type=ticket_type,
            price=price
        )
        print(f"Created ticket: {ticket.pk} for user {request.user.username}")
        
        messages.success(request, f"Successfully registered for {event.event_name}!")
        return redirect('user_dashboard')  # Adjust if your dashboard URL name is different
    
    context = {
        'event': event,
        'ticket_options': ticket_options
    }
    
    return render(request, 'register_event.html', context)
@login_required
def create_event(request):
    if request.method == 'POST':
        # Process form submission
        event_name = request.POST.get('event_name')
        event_type = request.POST.get('event_type')
        event_description = request.POST.get('event_description')
        event_location = request.POST.get('event_location')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        max_capacity = request.POST.get('max_capacity')
        
        # Create new event
        Event.objects.create(
            event_name=event_name,
            event_type=event_type,
            event_description=event_description,
            event_location=event_location,
            start_time=start_time,
            end_time=end_time,
            max_capacity=max_capacity,
            status='Upcoming'
        )
        
        messages.success(request, "Event created successfully!")
        return redirect('admin_dashboard')
    
    # Display empty form
    return render(request, 'create_event.html')

@login_required
def delete_event(request, event_id):
    # Get the event or return 404 if not found
    event = get_object_or_404(Event, event_id=event_id)
    
    # Security check - only staff should delete events
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to delete events.")
        return redirect('event_list')
    
    if request.method == 'POST':
        # Delete the event and redirect to admin dashboard
        event.delete()
        messages.success(request, f"Event '{event.event_name}' has been deleted.")
        return redirect('admin_dashboard')
    
    # Show confirmation page
    return render(request, 'delete_event.html', {'event': event})

# events/views.py
def edit_event(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    if request.method == 'POST':
        # Extract form data
        event.event_name = request.POST.get('event_name')
        event.event_type = request.POST.get('event_type')
        event.event_description = request.POST.get('event_description')
        event.event_location = request.POST.get('event_location')
        event.start_time = request.POST.get('start_time')
        event.end_time = request.POST.get('end_time')
        event.max_capacity = request.POST.get('max_capacity')
        
        # Save the updated event
        event.save()
        
        # Add a success message
        messages.success(request, "Event updated successfully!")
        
        # Redirect to event detail page
        return redirect('event_detail', event_id=event_id)
    
    return render(request, 'edit_event.html', {'event': event})

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'ticket_detail.html', {'ticket': ticket})


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})
