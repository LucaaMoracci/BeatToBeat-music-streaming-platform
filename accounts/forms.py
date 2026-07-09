from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'birth_date', 'favorite_genre']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Racconta qualcosa di te...'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
