from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import GenreForm, PlaylistForm, SongForm
from .models import Genre, Playlist, Song
from .permissions import CuratorOnlyMixin


class SongListView(LoginRequiredMixin, ListView):
    model = Song
    template_name = 'music/songs/list.html'
    context_object_name = 'songs'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('genre')
        query = self.request.GET.get('q', '').strip()
        genre_id = self.request.GET.get('genre', '')

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(artist__icontains=query))
        if genre_id:
            queryset = queryset.filter(genre_id=genre_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['current_q'] = self.request.GET.get('q', '')
        context['current_genre'] = self.request.GET.get('genre', '')
        return context


class SongDetailView(LoginRequiredMixin, DetailView):
    model = Song
    template_name = 'music/songs/detail.html'
    context_object_name = 'song'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_playlists'] = Playlist.objects.filter(
            owner=self.request.user
        ).exclude(songs=self.object)
        return context


class SongCreateView(LoginRequiredMixin, CuratorOnlyMixin, CreateView):
    model = Song
    form_class = SongForm
    template_name = 'music/songs/form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class SongUpdateView(LoginRequiredMixin, CuratorOnlyMixin, UpdateView):
    model = Song
    form_class = SongForm
    template_name = 'music/songs/form.html'


class SongDeleteView(LoginRequiredMixin, CuratorOnlyMixin, DeleteView):
    model = Song
    template_name = 'music/songs/delete.html'
    success_url = reverse_lazy('music:song_list')


class GenreListView(LoginRequiredMixin, CuratorOnlyMixin, ListView):
    model = Genre
    template_name = 'music/genres/list.html'
    context_object_name = 'genres'


class GenreCreateView(LoginRequiredMixin, CuratorOnlyMixin, CreateView):
    model = Genre
    form_class = GenreForm
    template_name = 'music/genres/form.html'
    success_url = reverse_lazy('music:genre_list')


class GenreUpdateView(LoginRequiredMixin, CuratorOnlyMixin, UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = 'music/genres/form.html'
    success_url = reverse_lazy('music:genre_list')


class GenreDeleteView(LoginRequiredMixin, CuratorOnlyMixin, DeleteView):
    model = Genre
    template_name = 'music/genres/delete.html'
    success_url = reverse_lazy('music:genre_list')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Impossibile eliminare un genere con brani associati.")
            return redirect('music:genre_list')


class PlaylistListView(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = 'music/playlists/list.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist
    template_name = 'music/playlists/detail.html'
    context_object_name = 'playlist'

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'music/playlists/form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'music/playlists/form.html'

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


class PlaylistDeleteView(LoginRequiredMixin, DeleteView):
    model = Playlist
    template_name = 'music/playlists/delete.html'
    success_url = reverse_lazy('music:playlist_list')

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


@login_required
def add_song_to_playlist(request, song_id):
    if request.method != 'POST':
        return redirect('music:song_detail', pk=song_id)

    song = get_object_or_404(Song, id=song_id)
    playlist = get_object_or_404(Playlist, id=request.POST.get('playlist_id'), owner=request.user)

    if playlist.songs.filter(id=song.id).exists():
        messages.info(request, f"'{song.title}' è già in {playlist.name}.")
    else:
        playlist.songs.add(song)
        messages.success(request, f"'{song.title}' aggiunto a {playlist.name}.")
    return redirect('music:song_detail', pk=song.id)


@login_required
def remove_song_from_playlist(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
    song = get_object_or_404(Song, id=song_id)
    if request.method == 'POST':
        playlist.songs.remove(song)
        messages.info(request, f"'{song.title}' rimosso da {playlist.name}.")
    return redirect('music:playlist_detail', pk=playlist.id)
