from django import forms

from .models import Comment, Song, Genre, Playlist


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Il tuo commento'}
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Scrivi un commento...'}),
        }


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre', 'duration', 'audio_file']
        help_texts = {
            'duration': 'Formato hh:mm:ss (es. 0:03:30).',
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'description']


class PlaylistForm(forms.ModelForm):
    VISIBILITY_CHOICES = [
        ('private', 'Privata'),
        ('public', 'Pubblica'),
        ('editorial', 'Editoriale'),
    ]
    visibility = forms.ChoiceField(
        choices=VISIBILITY_CHOICES,
        widget=forms.RadioSelect,
        label='Visibilità',
    )

    class Meta:
        model = Playlist
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Le playlist editoriali sono riservate a curator e admin.
        if not (self.user and self.user.is_curator):
            self.fields['visibility'].choices = self.VISIBILITY_CHOICES[:2]

        if self.instance and self.instance.pk:
            if self.instance.is_editorial:
                self.fields['visibility'].initial = 'editorial'
            elif self.instance.is_public:
                self.fields['visibility'].initial = 'public'
            else:
                self.fields['visibility'].initial = 'private'
        else:
            self.fields['visibility'].initial = 'private'

    def clean_visibility(self):
        visibility = self.cleaned_data['visibility']
        if visibility == 'editorial' and not (self.user and self.user.is_curator):
            raise forms.ValidationError("Non puoi creare playlist editoriali.")
        return visibility

    def save(self, commit=True):
        instance = super().save(commit=False)
        visibility = self.cleaned_data['visibility']
        instance.is_editorial = visibility == 'editorial'
        instance.is_public = visibility in ('public', 'editorial')
        if commit:
            instance.save()
            self.save_m2m()
        return instance
