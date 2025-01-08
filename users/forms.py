from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, TechnicianRequest

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'
        if commit:
            user.save()
        return user

class TechnicianRegistrationForm(UserCreationForm):
    experience = forms.CharField(widget=forms.Textarea)
    qualifications = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'experience', 'qualifications')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'technician'
        user.is_active = False  # Will be activated after approval
        if commit:
            user.save()
            TechnicianRequest.objects.create(
                user=user,
                experience=self.cleaned_data['experience'],
                qualifications=self.cleaned_data['qualifications']
            )
        return user 