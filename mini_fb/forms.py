from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'profile_image_url': forms.URLInput(attrs={'placeholder': 'Profile Image URL (optional)'}),
        }

class CreateStatusMessageForm(forms.ModelForm):
    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': False}),
        required=False,
        label='Upload Images'
    )

    class Meta:
        model = StatusMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3,
                'cols': 40,
                'placeholder': 'What\'s on your mind?'
            }),
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'profile_image_url': forms.URLInput(attrs={'placeholder': 'Profile Image URL (optional)'}),
        }