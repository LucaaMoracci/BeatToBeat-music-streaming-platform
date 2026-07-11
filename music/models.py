from django.conf import settings
from django.core.validators import FileExtensionValidator
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
    story = models.TextField(
        blank=True,
        help_text='Un breve racconto sul brano, mostrato nella sua pagina.',
    )
    audio_file = models.FileField(
        upload_to='songs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg', 'm4a'])],
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_songs',
        blank=True,
    )
    play_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return f'{self.artist} - {self.title}'

    def get_absolute_url(self):
        return reverse('music:song_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Commento di {self.author.username} su {self.song.title}'


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
    is_public = models.BooleanField(default=False)
    is_editorial = models.BooleanField(default=False)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='saved_playlists',
        blank=True,
    )
    collaborators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='collaborative_playlists',
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.owner})'

    def get_absolute_url(self):
        return reverse('music:playlist_detail', kwargs={'pk': self.pk})

    def can_edit(self, user):
        """L'owner, i collaboratori e gli admin possono modificare i brani."""
        if not user.is_authenticated:
            return False
        return (
            user == self.owner
            or user.is_superuser
            or self.collaborators.filter(pk=user.pk).exists()
        )


class ModerationReport(models.Model):
    """Registro di un commento rimosso da un moderatore, con la motivazione."""
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='moderation_reports',
    )
    comment_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reported_comments',
    )
    song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, blank=True)
    comment_text = models.TextField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Report di {self.moderator} il {self.created_at:%d/%m/%Y}'
