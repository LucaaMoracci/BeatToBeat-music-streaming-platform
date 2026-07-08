from django.contrib import admin

from .models import Genre, Song, Playlist


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'added_by', 'duration', 'created_at']
    list_filter = ['genre', 'created_at']
    search_fields = ['title', 'artist']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']
    list_filter = ['owner']
    search_fields = ['name']
    filter_horizontal = ['songs']
