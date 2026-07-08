from django import forms

from .models import Song, Genre, Playlist


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'genre', 'duration']
        help_texts = {
            'duration': 'Formato hh:mm:ss (es. 0:03:30).',
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'description']


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name']
