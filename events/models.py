from django.db import models

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100, null=False)
    event_type = models.CharField(max_length=50, null=False)
    event_description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    event_location = models.CharField(max_length=100, null=False)
    max_capacity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Upcoming')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.event_name


class Attendee(models.Model):
    attendee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

        
class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey('users.Attendee', on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=50, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.ticket_type} - {self.event.event_name}"
