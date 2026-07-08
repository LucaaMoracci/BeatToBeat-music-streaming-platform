from django.conf import settings
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('music:genre_list')


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        related_name='songs',
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='added_songs',
    )
    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f'{self.artist} - {self.title}'

    def get_absolute_url(self):
        return reverse('music:song_detail', kwargs={'pk': self.pk})


class Playlist(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='playlists',
    )
    songs = models.ManyToManyField(
        Song,
        related_name='playlists',
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.owner})'

    def get_absolute_url(self):
        return reverse('music:playlist_detail', kwargs={'pk': self.pk})
