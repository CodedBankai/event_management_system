from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Ticket
from .forms import EventForm
from users.models import Attendee


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


def admin_dashboard(request):
    if not request.user.is_staff:  # Ensure only admin users can access this view
        return render(request, '403.html', status=403)

    events = Event.objects.all()
    
    event_category_count = Event.objects.values('event_type').distinct().count()
    events_count = Event.objects.count()
    user_registrations_count = Attendee.objects.count()
    complete_events_count = Event.objects.filter(status='Completed').count()

    recent_users = Attendee.objects.order_by('-registration_date')[:10]

    context = {
        'events': events,
        'event_category_count': event_category_count,
        'events_count': events_count,
        'user_registrations_count': user_registrations_count,
        'complete_events_count': complete_events_count,
        'recent_users': recent_users,
    }
    return render(request, 'admin_dashboard.html', context)


def user_dashboard(request):
    if request.user.is_staff:  # Prevent admin users from accessing this view
        return render(request, '403.html', status=403)

    events = Event.objects.all()  # Fetch all events for browsing
    context = {
        'events': events,
    }
    return render(request, 'user_dashboard.html', context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    return render(request, 'event_detail.html', {'event': event})


TICKET_OPTIONS = [
    {'type': 'Standard', 'price': 49.99},
    {'type': 'Premium', 'price': 99.99},
    {'type': 'VIP', 'price': 149.99},
]


@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)

    if request.method == 'POST':
        # Check capacity limit before processing registration
        current_tickets = Ticket.objects.filter(event=event).count()
        if event.max_capacity is not None and current_tickets >= event.max_capacity:
            messages.error(request, "This event is full. We welcome you next time!")
            return redirect('user_dashboard')

        ticket_type = request.POST.get('ticket_type')

        price = None
        for option in TICKET_OPTIONS:
            if option['type'] == ticket_type:
                price = option['price']
                break

        if price is None:
            messages.error(request, "Please select a valid ticket type.")
            return render(request, 'register_event.html', {
                'event': event,
                'ticket_options': TICKET_OPTIONS,
            })

        # Get or create attendee record with explicit user link
        try:
            if hasattr(request.user, 'attendee') and request.user.attendee:
                attendee = request.user.attendee
            elif request.user.email:
                attendee = Attendee.objects.get(email=request.user.email)
                if not attendee.user:
                    attendee.user = request.user
                    attendee.save()
            else:
                raise Attendee.DoesNotExist
        except Attendee.DoesNotExist:
            email_to_use = request.user.email
            if not email_to_use:
                email_to_use = f"user_{request.user.id}@example.com"
            attendee = Attendee.objects.create(
                user=request.user,
                email=email_to_use,
                first_name=request.user.first_name or request.user.username,
                last_name=request.user.last_name or ''
            )

        Ticket.objects.create(
            event=event,
            attendee=attendee,
            ticket_type=ticket_type,
            price=price
        )

        messages.success(request, f"Successfully registered for {event.event_name}!")
        return redirect('user_dashboard')

    current_tickets = Ticket.objects.filter(event=event).count()
    is_full = False
    if event.max_capacity is not None and current_tickets >= event.max_capacity:
        is_full = True

    context = {
        'event': event,
        'ticket_options': TICKET_OPTIONS,
        'is_full': is_full,
    }

    return render(request, 'register_event.html', context)


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.status = 'Upcoming'
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('admin_dashboard')
        messages.error(request, "Please correct the errors below.")
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)

    if not request.user.is_staff:
        messages.error(request, "You don't have permission to delete events.")
        return redirect('event_list')

    if request.method == 'POST':
        event.delete()
        messages.success(request, f"Event '{event.event_name}' has been deleted.")
        return redirect('admin_dashboard')

    return render(request, 'delete_event.html', {'event': event})


def edit_event(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_detail', event_id=event_id)
        messages.error(request, "Please correct the errors below.")
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'event': event, 'form': form})


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    return render(request, 'ticket_detail.html', {'ticket': ticket})
