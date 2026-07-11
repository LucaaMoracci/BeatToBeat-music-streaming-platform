from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.sync_role_group()
        return response


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['liked_songs'] = user.liked_songs.all()[:5]
        context['liked_count'] = user.liked_songs.count()
        context['playlists'] = user.playlists.all()
        context['recent_comments'] = user.comments.select_related('song')[:5]
        context['comment_count'] = user.comments.count()
        context['play_history'] = user.play_history.select_related('song')[:5]
        context['history_count'] = user.play_history.count()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user


class PublicProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/public_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = self.object
        context['public_playlists'] = target.playlists.filter(
            Q(is_public=True) | Q(is_editorial=True)
        ).distinct()
        context['recent_comments'] = target.comments.all()[:5]
        return context


class LikedSongsView(LoginRequiredMixin, ListView):
    template_name = 'accounts/liked_songs.html'
    context_object_name = 'songs'
    paginate_by = 15

    def get_queryset(self):
        return self.request.user.liked_songs.select_related('genre')


class PlayHistoryView(LoginRequiredMixin, ListView):
    template_name = 'accounts/play_history.html'
    context_object_name = 'history'
    paginate_by = 20

    def get_queryset(self):
        return self.request.user.play_history.select_related('song')


class UserCommentsView(LoginRequiredMixin, ListView):
    template_name = 'accounts/user_comments.html'
    context_object_name = 'comments'
    paginate_by = 20

    def get_queryset(self):
        return self.request.user.comments.select_related('song')
