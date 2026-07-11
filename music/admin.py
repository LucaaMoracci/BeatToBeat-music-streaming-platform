from django.contrib import admin

from .models import Genre, ModerationReport, PlayHistory, Song, Playlist


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
    filter_horizontal = ['songs', 'collaborators', 'pending_collaborators']


@admin.register(ModerationReport)
class ModerationReportAdmin(admin.ModelAdmin):
    list_display = ['moderator', 'comment_author', 'song', 'created_at']
    list_filter = ['created_at', 'moderator']
    search_fields = ['reason', 'comment_text']


@admin.register(PlayHistory)
class PlayHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'song', 'played_at']
    list_filter = ['played_at', 'user']
    search_fields = ['song__title', 'user__username']
