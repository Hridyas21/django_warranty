from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CustomerRegistrationForm, TechnicianRegistrationForm
from .models import TechnicianRequest, User
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now login.')
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def technician_register(request):
    if request.method == 'POST':
        form = TechnicianRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your registration request has been submitted for approval.')
            return redirect('login')
    else:
        form = TechnicianRegistrationForm()
    return render(request, 'users/technician_register.html', {'form': form})

@user_passes_test(lambda u: u.role == 'admin')
def technician_requests(request):
    pending_requests = TechnicianRequest.objects.filter(is_approved=False)
    return render(request, 'users/technician_requests.html', {'requests': pending_requests})

@user_passes_test(lambda u: u.role == 'admin')
def approve_technician(request, request_id):
    tech_request = TechnicianRequest.objects.get(id=request_id)
    user = tech_request.user
    user.is_active = True
    user.is_approved = True
    user.save()
    tech_request.is_approved = True
    tech_request.save()
    messages.success(request, f'Technician {user.username} has been approved.')
    return redirect('technician_requests')

def handler403(request, exception):
    return render(request, 'users/403.html', status=403)

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
@never_cache
@require_http_methods(["POST"])
def logout_view(request):
    # Clear any session data
    request.session.flush()
    
    # Logout the user
    logout(request)
    
    response = redirect('login')
    
    # Clear all cookies
    for key in request.COOKIES:
        response.delete_cookie(key)
    
    # Set no-cache headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response
