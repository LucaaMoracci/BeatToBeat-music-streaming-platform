import os
from datetime import timedelta

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beattobeat.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone

from music.models import Comment, Genre, ModerationReport, PlayHistory, Playlist, Song

User = get_user_model()


ACCOUNTS = [
    ('admin_demo', 'admin@beattobeat.test', 'curator', True, 'admin12345'),
    ('curator_demo', 'curator@beattobeat.test', 'curator', False, 'curator12345'),
    ('moderator_demo', 'moderator@beattobeat.test', 'moderator', False, 'moderator12345'),
    ('listener_demo', 'listener@beattobeat.test', 'listener', False, 'listener12345'),
    ('alice', 'alice@beattobeat.test', 'listener', False, 'password123'),
    ('bob', 'bob@beattobeat.test', 'listener', False, 'password123'),
]

GENRES = ['Rock', 'Pop', 'Jazz', 'Electronic', 'Hip Hop', 'Classical']

SONGS = [
    ('Stairway to Heaven', 'Led Zeppelin', 'Rock', (8, 2)),
    ('Bohemian Rhapsody', 'Queen', 'Rock', (5, 55)),
    ('Smells Like Teen Spirit', 'Nirvana', 'Rock', (5, 1)),
    ('Billie Jean', 'Michael Jackson', 'Pop', (4, 54)),
    ('Shape of You', 'Ed Sheeran', 'Pop', (3, 53)),
    ('Take Five', 'Dave Brubeck', 'Jazz', (5, 24)),
    ('So What', 'Miles Davis', 'Jazz', (9, 22)),
    ('One More Time', 'Daft Punk', 'Electronic', (5, 20)),
    ('Strobe', 'deadmau5', 'Electronic', (10, 37)),
    ('Lose Yourself', 'Eminem', 'Hip Hop', (5, 26)),
    ('Juicy', 'The Notorious B.I.G.', 'Hip Hop', (5, 2)),
    ('Clair de Lune', 'Claude Debussy', 'Classical', (5, 5)),
]


def seed():
    users = {}
    for username, email, role, is_super, password in ACCOUNTS:
        user, _ = User.objects.get_or_create(username=username, defaults={'email': email})
        user.email = email
        user.role = role
        user.is_superuser = is_super
        user.is_staff = is_super
        user.set_password(password)
        user.save()
        user.sync_role_group()
        users[username] = user

    genres = {}
    for name in GENRES:
        genre, _ = Genre.objects.get_or_create(
            name=name,
            defaults={'description': f'Il meglio del genere {name}.'},
        )
        genres[name] = genre

    users['listener_demo'].bio = 'Ascolto un po\' di tutto, ma il rock resta il mio preferito.'
    users['listener_demo'].favorite_genre = genres['Rock']
    users['listener_demo'].save()
    users['alice'].bio = 'Fan sfegatata del rock classico.'
    users['alice'].favorite_genre = genres['Rock']
    users['alice'].save()
    users['bob'].favorite_genre = genres['Hip Hop']
    users['bob'].save()

    curator = users['curator_demo']
    songs = {}
    for title, artist, genre_name, (minutes, seconds) in SONGS:
        song, _ = Song.objects.get_or_create(
            title=title,
            artist=artist,
            defaults={
                'genre': genres[genre_name],
                'added_by': curator,
                'duration': timedelta(minutes=minutes, seconds=seconds),
            },
        )
        songs[title] = song

    # Due brani con audio reale riproducibile: la durata coincide con quella del
    # file, così l'auto-rilevamento della durata dal file è verificabile a colpo d'occhio.
    Song.objects.update(audio_file='')
    songs['Bohemian Rhapsody'].audio_file = 'audio/demo_track_1.wav'
    songs['Bohemian Rhapsody'].duration = timedelta(seconds=150)
    songs['Bohemian Rhapsody'].save()
    songs['Billie Jean'].audio_file = 'audio/demo_track_2.wav'
    songs['Billie Jean'].duration = timedelta(seconds=200)
    songs['Billie Jean'].save()

    STORIES = {
        'Bohemian Rhapsody': (
            'Registrata nel 1975, la canzone unisce ballata, opera e hard rock in quasi sei minuti. '
            'La sezione operistica richiese settimane di sovraincisioni vocali, tanto che il nastro '
            'consumato dalle registrazioni divenne quasi trasparente.'
        ),
        'Billie Jean': (
            'Il celebre giro di basso nacque da un\'idea che Michael Jackson canticchiava di continuo. '
            'Il produttore Quincy Jones voleva cambiarlo, ma Jackson insistette: quella linea sarebbe '
            'diventata una delle piu riconoscibili della storia del pop.'
        ),
    }
    for title, story in STORIES.items():
        songs[title].story = story
        songs[title].save()

    mix, _ = Playlist.objects.get_or_create(name='Il mio mix', owner=users['listener_demo'])
    mix.songs.set([songs['Bohemian Rhapsody'], songs['Billie Jean'], songs['Lose Yourself']])
    mix.collaborators.set([users['alice'], users['bob']])
    mix.pending_collaborators.set([users['curator_demo']])

    rock, _ = Playlist.objects.get_or_create(name='Rock Classics', owner=users['alice'])
    rock.is_public = True
    rock.save()
    rock.songs.set([s for s in songs.values() if s.genre.name == 'Rock'])
    rock.followers.set([users['listener_demo']])

    editorial, _ = Playlist.objects.get_or_create(name='Editors Picks', owner=users['curator_demo'])
    editorial.is_public = True
    editorial.is_editorial = True
    editorial.save()
    editorial.songs.set(list(songs.values())[:5])
    editorial.followers.set([users['listener_demo'], users['bob']])

    songs['Bohemian Rhapsody'].likes.set([users['listener_demo'], users['alice'], users['bob'], users['curator_demo']])
    songs['Billie Jean'].likes.set([users['listener_demo'], users['alice']])
    songs['Lose Yourself'].likes.set([users['bob']])

    for title, count in [('Bohemian Rhapsody', 128), ('Billie Jean', 94), ('Take Five', 61), ('Lose Yourself', 47), ('Stairway to Heaven', 39), ('Shape of You', 25)]:
        Song.objects.filter(pk=songs[title].pk).update(play_count=count)

    c1, _ = Comment.objects.get_or_create(song=songs['Bohemian Rhapsody'], author=users['alice'], text='Un capolavoro senza tempo.')
    c1.likes.set([users['bob'], users['listener_demo']])
    Comment.objects.get_or_create(song=songs['Bohemian Rhapsody'], author=users['bob'], text='La sezione operistica è pazzesca!')
    Comment.objects.get_or_create(song=songs['Billie Jean'], author=users['listener_demo'], text='Il basso più famoso della storia.')

    PlayHistory.objects.filter(user=users['listener_demo']).delete()
    now = timezone.now()
    plays = [
        ('Bohemian Rhapsody', 2),
        ('Billie Jean', 8),
        ('Lose Yourself', 35),
        ('Take Five', 90),
        ('Shape of You', 240),
        ('Bohemian Rhapsody', 1440),
    ]
    for title, minutes_ago in plays:
        entry = PlayHistory.objects.create(user=users['listener_demo'], song=songs[title])
        PlayHistory.objects.filter(pk=entry.pk).update(played_at=now - timedelta(minutes=minutes_ago))

    ModerationReport.objects.get_or_create(
        moderator=users['moderator_demo'],
        comment_author=users['bob'],
        song=songs['Bohemian Rhapsody'],
        comment_text='Compra follower a poco prezzo su spam-link.xyz!',
        defaults={'reason': 'Spam: link promozionale non consentito.'},
    )

    print(f'Dati creati: {len(users)} utenti, {len(genres)} generi, {len(songs)} brani, {Playlist.objects.count()} playlist.')


if __name__ == '__main__':
    seed()
