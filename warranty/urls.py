from django.contrib import admin
from django.urls import path, include
from users.views import home, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('users.urls')),
    path('logout/', logout_view, name='logout'),
]
