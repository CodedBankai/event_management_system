
from django.shortcuts import render, redirect
from django.contrib.auth import login ,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login  

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():  # Make sure these parentheses are here!
            user = form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        else:
            # Display form errors to the user
            messages.error(request, "Please correct the errors below.")
            print(form.errors)  # For debugging
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


# Change your view function name:
# Django's built-in login function

def login_view(request):
    # Initialize context with empty values
    context = {
        'username': '',
        'error': None
    }
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Save username to repopulate the form in case of errors
        context['username'] = username
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password")
            context['error'] = "Invalid username or password"
    
    # Return the context without any reference to 'form'
    return render(request, 'login.html', context)


@user_passes_test(lambda u: u.is_staff) 
def admin_dashboard(request):
    # Add your dashboard logic here
    return render(request, 'admin_dashboard.html')