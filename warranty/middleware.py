from django.shortcuts import redirect
from django.urls import reverse

class PreventBackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add no-cache headers to all responses
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        return response

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # Check if the request is for a protected URL
            protected_paths = [
                '/home/',  # Add your protected URLs here
                '/profile/',
                '/dashboard/',
            ]
            
            if any(request.path.startswith(path) for path in protected_paths):
                return redirect('login')
        
        response = self.get_response(request)
        return response 