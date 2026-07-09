from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        LISTENER = 'listener', 'Listener'
        CURATOR = 'curator', 'Curator'
        MODERATOR = 'moderator', 'Moderator'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.LISTENER,
    )
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    favorite_genre = models.ForeignKey(
        'music.Genre',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fans',
    )

    AVATAR_COLORS = ['#f0803c', '#e0a15e', '#81b29a', '#6a8ec9', '#b07ba0', '#c96a6a']

    @property
    def avatar_color(self):
        return self.AVATAR_COLORS[sum(ord(c) for c in self.username) % len(self.AVATAR_COLORS)]

    @property
    def initial(self):
        return self.username[0].upper() if self.username else '?'

    @property
    def is_curator(self):
        return self.role == self.Role.CURATOR or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR or self.is_superuser

    def sync_role_group(self):
        role_groups = Group.objects.filter(name__in=[r.label for r in self.Role])
        self.groups.remove(*role_groups)
        group, _ = Group.objects.get_or_create(name=self.get_role_display())
        self.groups.add(group)

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
