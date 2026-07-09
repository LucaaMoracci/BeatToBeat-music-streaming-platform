from django.contrib.auth import views as auth_views
from django.urls import path

from .views import ProfileUpdateView, PublicProfileView, SignUpView, UserProfileView

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('u/<str:username>/', PublicProfileView.as_view(), name='public_profile'),
]
