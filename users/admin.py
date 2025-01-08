from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TechnicianRequest

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'is_active', 'date_joined')
    list_filter = ('role', 'is_approved', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('role', 'is_approved', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_approved'),
        }),
    )

class TechnicianRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_approved', 'get_email')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('user__username', 'user__email', 'experience', 'qualifications')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        for tech_request in queryset:
            user = tech_request.user
            user.is_active = True
            user.is_approved = True
            user.save()
            tech_request.is_approved = True
            tech_request.save()
        self.message_user(request, f"{queryset.count()} technician request(s) were successfully approved.")
    approve_requests.short_description = "Approve selected technician requests"
    
    def reject_requests(self, request, queryset):
        queryset.update(is_approved=False)
        users = User.objects.filter(technicianrequest__in=queryset)
        users.update(is_active=False, is_approved=False)
        self.message_user(request, f"{queryset.count()} technician request(s) were rejected.")
    reject_requests.short_description = "Reject selected technician requests"

# Register the models with their respective admin classes
admin.site.register(User, CustomUserAdmin)
admin.site.register(TechnicianRequest, TechnicianRequestAdmin)
