from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CommentForm, GenreForm, PlaylistForm, SongForm
from .models import Comment, Genre, Playlist, Song
from .permissions import CuratorOnlyMixin


class SongListView(LoginRequiredMixin, ListView):
    model = Song
    template_name = 'music/songs/list.html'
    context_object_name = 'songs'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('genre')
        query = self.request.GET.get('q', '').strip()
        genre_id = self.request.GET.get('genre', '')
        has_audio = self.request.GET.get('has_audio')

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(artist__icontains=query))
        if genre_id:
            queryset = queryset.filter(genre_id=genre_id)
        if has_audio:
            queryset = queryset.exclude(audio_file='').exclude(audio_file__isnull=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['current_q'] = self.request.GET.get('q', '')
        context['current_genre'] = self.request.GET.get('genre', '')
        context['current_has_audio'] = self.request.GET.get('has_audio')
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
        context['comment_form'] = CommentForm()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['editorial_playlists'] = Playlist.objects.filter(is_editorial=True).exclude(owner=user)
        context['saved_playlists'] = user.saved_playlists.all()
        return context


class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist
    template_name = 'music/playlists/detail.html'
    context_object_name = 'playlist'

    def get_queryset(self):
        # L'owner vede sempre la propria; le altre solo se pubbliche o editoriali.
        return Playlist.objects.filter(
            Q(owner=self.request.user) | Q(is_public=True) | Q(is_editorial=True)
        ).distinct()


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'music/playlists/form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'music/playlists/form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


class PlaylistDeleteView(LoginRequiredMixin, DeleteView):
    model = Playlist
    template_name = 'music/playlists/delete.html'
    success_url = reverse_lazy('music:playlist_list')

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


@login_required
def toggle_like_song(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        if request.user in song.likes.all():
            song.likes.remove(request.user)
        else:
            song.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER') or song.get_absolute_url())


@login_required
def add_comment(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.song = song
            comment.author = request.user
            comment.save()
    return redirect('music:song_detail', pk=song.pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if not request.user.is_moderator:
        raise PermissionDenied
    song_pk = comment.song.pk
    if request.method == 'POST':
        comment.delete()
    return redirect('music:song_detail', pk=song_pk)


@login_required
def toggle_like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER') or comment.song.get_absolute_url())


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


@login_required
def toggle_save_playlist(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    # Si possono salvare solo playlist pubbliche o editoriali non proprie.
    if playlist.owner == request.user or not (playlist.is_public or playlist.is_editorial):
        raise PermissionDenied
    if request.method == 'POST':
        if request.user in playlist.followers.all():
            playlist.followers.remove(request.user)
        else:
            playlist.followers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER') or playlist.get_absolute_url())
