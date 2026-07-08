from django.db import migrations


def create_moderator_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Moderator')


def remove_moderator_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='Moderator').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_role'),
    ]

    operations = [
        migrations.RunPython(create_moderator_group, remove_moderator_group),
    ]
