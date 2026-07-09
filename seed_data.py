import os
from datetime import timedelta

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beattobeat.settings')
django.setup()

from django.contrib.auth import get_user_model

from music.models import Comment, Genre, Playlist, Song

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

    for title in ('Bohemian Rhapsody', 'Billie Jean', 'Take Five'):
        songs[title].audio_file = 'songs/demo_tone.wav'
        songs[title].save()

    mix, _ = Playlist.objects.get_or_create(name='Il mio mix', owner=users['listener_demo'])
    mix.songs.set([songs['Bohemian Rhapsody'], songs['Billie Jean'], songs['Lose Yourself']])

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

    c1, _ = Comment.objects.get_or_create(song=songs['Bohemian Rhapsody'], author=users['alice'], text='Un capolavoro senza tempo.')
    c1.likes.set([users['bob'], users['listener_demo']])
    Comment.objects.get_or_create(song=songs['Bohemian Rhapsody'], author=users['bob'], text='La sezione operistica è pazzesca!')
    Comment.objects.get_or_create(song=songs['Billie Jean'], author=users['listener_demo'], text='Il basso più famoso della storia.')

    print(f'Dati creati: {len(users)} utenti, {len(genres)} generi, {len(songs)} brani, {Playlist.objects.count()} playlist.')


if __name__ == '__main__':
    seed()
