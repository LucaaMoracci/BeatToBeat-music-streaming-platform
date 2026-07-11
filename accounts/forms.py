from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nome utente'
        self.fields['username'].help_text = ''
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = ''
        self.fields['password2'].label = 'Conferma password'
        self.fields['password2'].help_text = 'Inserisci di nuovo la stessa password, per verifica.'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar_image', 'bio', 'birth_date', 'favorite_genre']
        labels = {'avatar_image': 'Immagine profilo'}
        help_texts = {'avatar_image': 'Lascia vuoto per usare l\'avatar con l\'iniziale.'}
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Racconta qualcosa di te...'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
