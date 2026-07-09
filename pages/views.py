from django.db.models import Count
from django.views.generic import TemplateView

from music.models import Song


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['latest_songs'] = Song.objects.all()[:6]
            context['popular_songs'] = Song.objects.annotate(
                num_likes=Count('likes')
            ).order_by('-num_likes', '-created_at')[:6]
            if user.favorite_genre_id:
                context['favorite_genre'] = user.favorite_genre
                context['genre_songs'] = Song.objects.filter(genre=user.favorite_genre)[:6]
        return context
