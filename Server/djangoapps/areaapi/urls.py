"""
URL configuration for incomeexpensesapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from github_webhook import viewss
from about_json import viewses
from google_auth import google_views
from youtube_spotify.views import *


from trello.views import *
from dog.views import *
from newsapi.views import *
from jokes.views import *
from opentrivia.views import *
from reddit.views import *
from bible.views import *
from weather_api.views import *

from authentication.views import RegisterView, LoginAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
      title="AREA PROJECT API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.areacom/policies/terms/",
      contact=openapi.Contact(email="contact@expenses.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
     path('register', RegisterView.as_view(), name="register"),
    path('login', LoginAPIView.as_view(), name="login"),
    path('about.json/', viewses.about_json),
    path('send-email/', viewss.send_email),
    path('hello/', viewss.hello),
    path('github/', viewss.get_github_auth),
    path('github_callback/', viewss.github_callback),
    path('github/create_repo/', viewss.create_github_repo),
    path('github/create_issues/', viewss.create_issues),
    path('google/auth/', google_views.google_authentification),
    path('google/callback/', google_views.google_authentification_callback),
    path('trello/', viewss.trello_user_auth),
    path('trello-auth/', viewss.trello_user_token),

    path('spotify/login/', spotify_login, name='spotify_login'),
    path('callback', spotify_callback, name='spotify_callback'),
    path('add/<str:video_title>/', add_song_to_spotify_playlist, name='add_song_to_spotify_playlist'),
    path('mail/', send_email, name='send_email'),
    path('add_playlist/<str:video_title>/', send_email2, name='send_email2'), ##ajoute un song dans un playlist et otifie directement par mail

    path('dog/image/', random_dog_uri),
    path('dog/collection/', random_dogs_uri),
    path('dog/breeds/', random_breed_name),
    path('jokes/', random_jokes),
    path('news_topic/', random_topic),
    path('biblical_passage/', get_bible_verse),
    path('reddit/inquiry/', ask_question),
    path('reddit/article/', article_publication),
   # path('select_sity/', get_weather),
    path('cities/', get_all_benin_cities),
    path('send_email_weather/', send_email_weather)
]
