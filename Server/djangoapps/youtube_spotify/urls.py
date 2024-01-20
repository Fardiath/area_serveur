# urls.py (de votre application)

from django.urls import path
from .views import ma_vue
# from .views import spotify_login
# from .views import spotify_callback
# from .views import get_youtube_video_info
# from .views import redirect_to_spotify_auth
# from .views import get_spotify_access_token

urlpatterns = [
    # path('spotify/login/', spotify_login, name='spotify_login'),
    path('/', ma_vue, name='ma_vue'),
    # path('callback/', spotify_callback, name='spotify_callback'),
    # path('youtube', get_youtube_video_info, name='get_youtube_video_info'),
    # path('spotify/authorize/', get_spotify_access_token, name='get_spotify_access_token'),
    # path('callback/', redirect_to_spotify_auth, name='redirect_to_spotify_auth'),
    # path('like-youtube/str<video_id>', get_youtube_video_info, name='get_youtube_video_info'),
]
