from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        LISTENER = 'listener', 'Listener'
        CURATOR = 'curator', 'Curator'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.LISTENER,
    )

    @property
    def is_curator(self):
        return self.role == self.Role.CURATOR or self.is_superuser

    def sync_role_group(self):
        role_groups = Group.objects.filter(name__in=[r.label for r in self.Role])
        self.groups.remove(*role_groups)
        group, _ = Group.objects.get_or_create(name=self.get_role_display())
        self.groups.add(group)

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
