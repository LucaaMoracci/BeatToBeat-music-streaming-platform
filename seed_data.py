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

STORIES = {
    'Stairway to Heaven': (
        "Composta nel 1971, cresce lentamente da un arpeggio acustico fino a un finale elettrico. "
        "Jimmy Page la mise a punto in un cottage gallese senza corrente, lontano dalle distrazioni della città."
    ),
    'Bohemian Rhapsody': (
        "Registrata nel 1975, unisce ballata, opera e hard rock in quasi sei minuti. La sezione operistica "
        "richiese settimane di sovraincisioni vocali, tanto che il nastro consumato divenne quasi trasparente."
    ),
    'Smells Like Teen Spirit': (
        "Il riff nacque quasi per gioco, ispirato all'alternanza piano-forte dei Pixies. Divenne l'inno di una "
        "generazione quasi contro la volontà della band, sorpresa dal successo planetario."
    ),
    'Billie Jean': (
        "Il celebre giro di basso nacque da un'idea che Michael Jackson canticchiava di continuo. Quincy Jones "
        "voleva cambiarlo, ma Jackson insistette: quella linea sarebbe diventata una delle più riconoscibili del pop."
    ),
    'Shape of You': (
        "Pensata inizialmente per un'altra artista, Ed Sheeran decise di tenerla per sé. Il giro percussivo e il "
        "ritornello immediato ne fecero uno dei singoli più ascoltati di sempre in streaming."
    ),
    'Take Five': (
        "In un insolito tempo di 5/4, nacque come esperimento ritmico del quartetto di Dave Brubeck. Contro ogni "
        "previsione, divenne il brano jazz strumentale più venduto della storia."
    ),
    'So What': (
        "Due soli accordi e un'enorme libertà: è il manifesto del jazz modale. Miles Davis lo incise in poche "
        "riprese, lasciando ampio spazio all'improvvisazione dei musicisti."
    ),
    'One More Time': (
        "La voce filtrata col vocoder è un omaggio alla dance francese. I Daft Punk cercavano il suono di una "
        "festa infinita, e il risultato divenne subito un classico da pista."
    ),
    'Strobe': (
        "Oltre dieci minuti che salgono con pazienza fino a esplodere. deadmau5 la pensò come un viaggio più che "
        "come una canzone, e la usa spesso per chiudere i suoi concerti."
    ),
    'Lose Yourself': (
        "Scritta sul set del film 8 Mile, cattura la tensione dell'attimo prima di salire sul palco. Eminem la "
        "incise tra una ripresa e l'altra, e gli valse un premio Oscar."
    ),
    'Juicy': (
        "Il racconto in musica della scalata dalla povertà al successo. The Notorious B.I.G. trasformò la propria "
        "biografia in un inno di riscatto tuttora amatissimo."
    ),
    'Clair de Lune': (
        "Terzo movimento della Suite bergamasque, evoca il chiaro di luna con delicatezza impressionista. Debussy "
        "la rivide per anni prima di pubblicarla, cercando la massima leggerezza."
    ),
}

# (playlist, brani, opzioni). editorial implica pubblica.
PLAYLISTS = [
    ('Il mio mix', 'listener_demo', ['Bohemian Rhapsody', 'Billie Jean', 'Lose Yourself'],
     dict(collaborators=['alice', 'bob'], pending=['curator_demo'])),
    ('Rock Classics', 'alice', ['Stairway to Heaven', 'Bohemian Rhapsody', 'Smells Like Teen Spirit'],
     dict(public=True, followers=['listener_demo', 'bob'])),
    ('Editors Picks', 'curator_demo',
     ['Bohemian Rhapsody', 'Billie Jean', 'Take Five', 'One More Time', 'Lose Yourself'],
     dict(editorial=True, followers=['listener_demo', 'bob', 'alice'])),
    ('Chill del pomeriggio', 'listener_demo', ['Clair de Lune', 'Take Five', 'So What'],
     dict(public=True, followers=['alice'])),
    ('Solo Jazz', 'bob', ['Take Five', 'So What'],
     dict(public=True, followers=['listener_demo', 'alice'])),
    ('Notti elettroniche', 'alice', ['One More Time', 'Strobe'],
     dict(collaborators=['listener_demo'])),
    ('Piano e quiete', 'curator_demo', ['Clair de Lune'],
     dict(editorial=True, followers=['alice'])),
    ('Carica da palestra', 'bob', ['Lose Yourself', 'Smells Like Teen Spirit', 'One More Time'],
     dict(public=True, followers=['listener_demo'])),
]

LIKES = {
    'Bohemian Rhapsody': ['listener_demo', 'alice', 'bob', 'curator_demo'],
    'Billie Jean': ['listener_demo', 'alice', 'bob'],
    'Lose Yourself': ['bob', 'listener_demo'],
    'Stairway to Heaven': ['alice', 'bob'],
    'Take Five': ['listener_demo', 'curator_demo'],
    'One More Time': ['alice', 'bob', 'listener_demo'],
    'Clair de Lune': ['alice', 'listener_demo'],
    'So What': ['curator_demo'],
    'Strobe': ['bob'],
    'Shape of You': ['alice'],
}

PLAYS = {
    'Bohemian Rhapsody': 128, 'Billie Jean': 94, 'Stairway to Heaven': 73, 'Smells Like Teen Spirit': 66,
    'Take Five': 61, 'One More Time': 52, 'Lose Yourself': 47, 'Clair de Lune': 44,
    'Strobe': 38, 'Juicy': 31, 'So What': 29, 'Shape of You': 25,
}

# (brano, autore, testo, chi mette like)
COMMENTS = [
    ('Bohemian Rhapsody', 'alice', "Un capolavoro senza tempo.", ['bob', 'listener_demo']),
    ('Bohemian Rhapsody', 'bob', "La sezione operistica è pazzesca!", ['curator_demo']),
    ('Bohemian Rhapsody', 'curator_demo', "Ogni sezione è un piccolo mondo a sé.", ['listener_demo']),
    ('Billie Jean', 'listener_demo', "Il basso più famoso della storia.", ['alice']),
    ('Billie Jean', 'bob', "Quel video ha cambiato la TV per sempre.", ['alice']),
    ('Stairway to Heaven', 'bob', "Quel finale mi mette i brividi ogni volta.", ['alice', 'listener_demo']),
    ('Smells Like Teen Spirit', 'alice', "Gli anni 90 in poco più di quattro minuti.", ['bob']),
    ('Take Five', 'listener_demo', "Il 5/4 non è mai stato così elegante.", []),
    ('So What', 'curator_demo', "Due accordi e infinite possibilità.", ['bob']),
    ('One More Time', 'bob', "Impossibile restare fermi.", ['alice', 'listener_demo']),
    ('Lose Yourself', 'listener_demo', "Motivazione allo stato puro.", ['bob']),
    ('Shape of You', 'alice', "Ce l'ho in testa da giorni!", []),
    ('Strobe', 'bob', "Dieci minuti che volano.", ['listener_demo']),
    ('Strobe', 'alice', "Da ascoltare a volume alto.", []),
    ('Clair de Lune', 'alice', "Perfetta per rilassarsi la sera.", ['listener_demo', 'bob']),
    ('Juicy', 'listener_demo', "Un vero inno di riscatto.", []),
]

# cronologia ascolti per utente: (brano, minuti fa)
HISTORY = {
    'listener_demo': [
        ('Bohemian Rhapsody', 2), ('Billie Jean', 8), ('Lose Yourself', 35),
        ('Take Five', 90), ('Shape of You', 240), ('Bohemian Rhapsody', 1440),
    ],
    'alice': [
        ('Stairway to Heaven', 5), ('Clair de Lune', 60),
        ('One More Time', 300), ('Smells Like Teen Spirit', 720),
    ],
    'bob': [
        ('Lose Yourself', 12), ('Juicy', 90), ('So What', 600), ('One More Time', 1500),
    ],
}

# commenti già rimossi da un moderatore: (moderatore, autore, brano, testo, motivazione)
REPORTS = [
    ('moderator_demo', 'bob', 'Bohemian Rhapsody',
     "Compra follower a poco prezzo su spam-link.xyz!",
     "Spam: link promozionale non consentito."),
    ('moderator_demo', 'alice', 'Billie Jean',
     "Questo brano fa schifo e chi lo ascolta pure.",
     "Linguaggio offensivo verso altri utenti."),
    ('admin_demo', 'bob', 'Take Five',
     "Seguitemi sul mio canale, metto musica meglio di questa!",
     "Autopromozione ripetuta e fuori tema."),
    ('moderator_demo', 'alice', 'Lose Yourself',
     "aaaaaa primo!!!! aaaaa",
     "Commento privo di contenuto (flood)."),
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

    avatars = {
        'listener_demo': 'avatars/avatar_listener.png',
        'curator_demo': 'avatars/avatar_curator.png',
        'alice': 'avatars/avatar_alice.png',
    }
    for username, path in avatars.items():
        users[username].avatar_image = path
        users[username].save()

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

    # Due brani con audio riproducibile: la durata coincide con quella del
    # file, così l'auto-rilevamento della durata dal file è verificabile
    Song.objects.update(audio_file='')
    songs['Bohemian Rhapsody'].audio_file = 'audio/demo_track_1.wav'
    songs['Bohemian Rhapsody'].duration = timedelta(seconds=150)
    songs['Bohemian Rhapsody'].save()
    songs['Billie Jean'].audio_file = 'audio/demo_track_2.wav'
    songs['Billie Jean'].duration = timedelta(seconds=200)
    songs['Billie Jean'].save()

    for title, story in STORIES.items():
        songs[title].story = story
        songs[title].save()

    for name, owner, song_titles, opts in PLAYLISTS:
        playlist, _ = Playlist.objects.get_or_create(name=name, owner=users[owner])
        playlist.is_editorial = opts.get('editorial', False)
        playlist.is_public = opts.get('public', False) or playlist.is_editorial
        playlist.save()
        playlist.songs.set([songs[t] for t in song_titles])
        playlist.followers.set([users[u] for u in opts.get('followers', [])])
        playlist.collaborators.set([users[u] for u in opts.get('collaborators', [])])
        playlist.pending_collaborators.set([users[u] for u in opts.get('pending', [])])

    for title, likers in LIKES.items():
        songs[title].likes.set([users[u] for u in likers])

    for title, count in PLAYS.items():
        Song.objects.filter(pk=songs[title].pk).update(play_count=count)

    for song_title, author, text, likers in COMMENTS:
        comment, _ = Comment.objects.get_or_create(
            song=songs[song_title], author=users[author], text=text)
        comment.likes.set([users[u] for u in likers])

    now = timezone.now()
    for username, plays in HISTORY.items():
        PlayHistory.objects.filter(user=users[username]).delete()
        for title, minutes_ago in plays:
            entry = PlayHistory.objects.create(user=users[username], song=songs[title])
            PlayHistory.objects.filter(pk=entry.pk).update(
                played_at=now - timedelta(minutes=minutes_ago))

    for mod, author, song_title, comment_text, reason in REPORTS:
        ModerationReport.objects.get_or_create(
            moderator=users[mod],
            comment_author=users[author],
            song=songs[song_title],
            comment_text=comment_text,
            defaults={'reason': reason},
        )

    print(
        f'Dati creati: {len(users)} utenti, {len(genres)} generi, {len(songs)} brani, '
        f'{Playlist.objects.count()} playlist, {Comment.objects.count()} commenti, '
        f'{ModerationReport.objects.count()} report.'
    )


if __name__ == '__main__':
    seed()
