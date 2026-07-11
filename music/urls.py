from django.urls import path

from . import views

app_name = 'music'

urlpatterns = [
    path('songs/', views.SongListView.as_view(), name='song_list'),
    path('songs/add/', views.SongCreateView.as_view(), name='song_create'),
    path('songs/<int:pk>/', views.SongDetailView.as_view(), name='song_detail'),
    path('songs/<int:pk>/edit/', views.SongUpdateView.as_view(), name='song_update'),
    path('songs/<int:pk>/delete/', views.SongDeleteView.as_view(), name='song_delete'),
    path('songs/<int:pk>/like/', views.toggle_like_song, name='toggle_like_song'),
    path('songs/<int:pk>/played/', views.register_play, name='register_play'),
    path('songs/<int:song_id>/add-to-playlist/', views.add_song_to_playlist, name='add_to_playlist'),

    path('songs/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('moderation/', views.moderation_log, name='moderation_log'),
    path('comments/<int:pk>/like/', views.toggle_like_comment, name='toggle_like_comment'),

    path('genres/', views.GenreListView.as_view(), name='genre_list'),
    path('genres/add/', views.GenreCreateView.as_view(), name='genre_create'),
    path('genres/<int:pk>/edit/', views.GenreUpdateView.as_view(), name='genre_update'),
    path('genres/<int:pk>/delete/', views.GenreDeleteView.as_view(), name='genre_delete'),

    path('playlists/', views.PlaylistListView.as_view(), name='playlist_list'),
    path('playlists/add/', views.PlaylistCreateView.as_view(), name='playlist_create'),
    path('playlists/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist_detail'),
    path('playlists/<int:pk>/edit/', views.PlaylistUpdateView.as_view(), name='playlist_update'),
    path('playlists/<int:pk>/delete/', views.PlaylistDeleteView.as_view(), name='playlist_delete'),
    path('playlists/<int:playlist_id>/remove/<int:song_id>/', views.remove_song_from_playlist, name='remove_from_playlist'),
    path('playlists/<int:pk>/save/', views.toggle_save_playlist, name='toggle_save_playlist'),
    path('playlists/<int:pk>/add-song/', views.playlist_add_song, name='playlist_add_song'),
    path('playlists/<int:pk>/collaborators/add/', views.add_collaborator, name='add_collaborator'),
    path('playlists/<int:pk>/collaborators/<int:user_id>/remove/', views.remove_collaborator, name='remove_collaborator'),
]
