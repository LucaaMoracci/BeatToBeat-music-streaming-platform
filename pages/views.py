from django.db.models import Count
from django.shortcuts import redirect
from django.views.generic import TemplateView

from music.models import PlayHistory, Song


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Brani ascoltati di recente, senza ripetizioni
        recent = []
        seen = set()
        history = PlayHistory.objects.filter(user=user).select_related(
            'song', 'song__genre'
        ).order_by('-played_at', '-id')[:60]
        for entry in history:
            if entry.song_id not in seen:
                seen.add(entry.song_id)
                recent.append(entry.song)
            if len(recent) >= 6:
                break
        context['recently_played'] = recent

        context['latest_songs'] = Song.objects.all()[:6]
        context['popular_songs'] = Song.objects.annotate(
            num_likes=Count('likes')
        ).order_by('-num_likes', '-created_at')[:6]
        if user.favorite_genre_id:
            context['favorite_genre'] = user.favorite_genre
            context['genre_songs'] = Song.objects.filter(genre=user.favorite_genre)[:6]
        return context
