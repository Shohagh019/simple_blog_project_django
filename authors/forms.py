from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from . models import Profile

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'id': 'required'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'id': 'required'})
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'id': 'required', 'placeholder': 'e.g. +1234567890'})
    )
    birthdate = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'id': 'required'})
    )
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'phone_number', 'email', 'birthdate',
            'password1', 'password2', 'profile_image'
        ]

    def save(self, commit=True):
        # Save the user and set standard fields
        user = super().save(commit=commit)

        # Now create or update the profile
        profile_image = self.cleaned_data.get('profile_image')
        phone_number = self.cleaned_data.get('phone_number')
        birthdate = self.cleaned_data.get('birthdate')

        # Ensure the profile exists (created via signal or manually)
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'profile_image': profile_image,
                'phone_number': phone_number,
                'birthdate': birthdate
            }
        )

        return user

class UserUpdateForm(UserChangeForm):
    password = None  # Hide the password field (optional)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
    