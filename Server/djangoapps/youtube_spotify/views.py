from django.shortcuts import render, redirect
from .models import MaEntite
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests
from django.http import JsonResponse, HttpResponse
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import spotipy as sp_oauth
from django.http import HttpResponseBadRequest
import json
from django.core.mail import EmailMessage

# from googleapiclient.discovery import build

def ma_vue(request):
    entites = MaEntite.objects.all()
    return render(request, 'ma_template.html', {'enitites': entites})

def spotify_login(request):
    redirect_uri='http://13.48.177.31:8080/callback',
    # print("sp_oauth:", sp_oauth)
    auth_url = f'https://accounts.spotify.com/authorize?client_id=007d1919ecc74751b8ce19533c7a3fc0&redirect_uri={redirect_uri}&scope=user-read-private%20user-read-email'
    print("auth_url", auth_url)
    return redirect(auth_url)

def spotify_callback(request):
    code = request.GET.get('code')
    redirect_uri='http://13.48.177.31:8080/callback'
    token_url='https://accounts.spotify.com/api/token'
    print('code:', code)
    
    payload = {
        'client_id':"007d1919ecc74751b8ce19533c7a3fc0",
        'client_secret':"874330f87199446babfed6beb9340245",
        'code': code,
        'redirect_uri': redirect_uri
    }
    headers = {'Accept': 'application/json'}
    response = requests.post(token_url, data=payload, headers=headers)
    token_info = response.json().get('access_token')
    setCookie = HttpResponse('cookie set!')
    setCookie.set_cookie('spotify_token', token_info, max_age=21600)
    return setCookie


def google_auth(request):
    flow = InstalledAppFlow.from_client_secrets_file(
        './client_secret.json',  # Chemin vers votre fichier client_secret.json
        scopes=[
                'https://www.googleapis.com/auth/youtube',
                'https://www.googleapis.com/auth/youtube.channel-memberships.creator',
                'https://www.googleapis.com/auth/youtube.upload',
                'https://www.googleapis.com/auth/youtubepartner-channel-audit',
                'https://www.googleapis.com/auth/youtube.force-ssl',
                'https://www.googleapis.com/auth/youtube.readonly',
                'https://www.googleapis.com/auth/youtubepartner',
            ],
    )
    flow.redirect_uri = 'http://localhost:8080/youtube/callback/'
    print("redirect:", flow.redirect_uri)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
    )

    request.session['oauth_state'] = state
    print('authorization:', authorization_url)
    return redirect(authorization_url)


def google_auth_callback(request):
    # if 'oauth_state' not in request.session or 'state' not in request.GET or request.session['oauth_state'] != request.GET['state']:
    #     print('CODE')
    #     return HttpResponse('error_page')
    flow = InstalledAppFlow.from_client_secrets_file(
        './client_secret.json',
         scopes=[
                'https://www.googleapis.com/auth/youtube',
                'https://www.googleapis.com/auth/youtube.channel-memberships.creator',
                'https://www.googleapis.com/auth/youtube.upload',
                'https://www.googleapis.com/auth/youtubepartner-channel-audit',
                'https://www.googleapis.com/auth/youtube.force-ssl',
                'https://www.googleapis.com/auth/youtube.readonly',
                'https://www.googleapis.com/auth/youtubepartner',
            ],
    )
    flow.redirect_uri = 'http://localhost:8080/youtube/callback/'
    
    flow.fetch_token(code=request.GET['code'])
    credentials = flow.credentials
    print("TOKEN:", credentials.token)

    print('REFRESH:', credentials.refresh_token)
    # Save the credentials to use in future API requests
    # You may want to store these credentials securely, such as in a database
    # For simplicity, we're storing them in the session in this example
    request.session['google_credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }
    Cookieytb = HttpResponse('cookie youtube set!')
    Cookieytb.set_cookie('token', credentials.token, max_age=21600)
    return Cookieytb


def spotify_user_id(request):
    access_token = request.COOKIES.get('spotify_token')
    sp = Spotify(auth=access_token)
    user_info = sp.current_user()
    spotify_user_id = user_info['id']
    return spotify_user_id

def create_spotify_playlist_1(request):
    sp_oauth = SpotifyOAuth(
        settings.SPOTIFY_CLIENT_ID,
        settings.SPOTIFY_CLIENT_SECRET,
        settings.SPOTIFY_REDIRECT_URI,
        scope='playlist-modify-public playlist-modify-private',
    )
    
    # Obtenez le jeton d'accès OAuth
    token_info = request.COOKIES.get('spotify_token')
    
    if token_info:
        sp = Spotify(auth=token_info)
        id = spotify_user_id(request)
        
        print("id:", id)
        
        # creer playlist
        playlist_name = 'Chansons écoutées'
        # playlist_description = 'Playlist créée à partir de Django'
        playlist = sp.user_playlist_create(id, playlist_name, public=True)
        print('c')
        return playlist['id']
    else:
        return HttpResponse("Erreur d'authentification Spotify.")

# def get_youtube_liked(token):
#     # token = request.COOKIES.get('token')
#     api_url = 'https://www.googleapis.com/youtube/v3/videos'
#     params = {
#         'part': 'snippet',
#         'myRating': 'like',
#         'max_results': 50,
#     }
#     headers = {
#         'Authorization': f'Bearer {token}',
#     }

#     response = requests.get(api_url, params=params, headers=headers)

#     if response.status_code == 200:
#         liked_videos = response.json()['items']
#         return liked_videos
#     else:
#         return None

# def get_youtube_liked_songs(request):
    
#     token = request.COOKIES.get('token')
#     liked_videos = get_youtube_liked(token)
#     print("liked_videos:", liked_videos)

#     # Formattez les vidéos aimées pour les afficher dans la réponse
#     formatted_liked_videos = "\n".join([f"{video['snippet']['title']} - {video['id']}" for video in liked_videos])

#     # Renvoyez la réponse avec les vidéos aimées formatées
#     print(f"Vidéos aimées :\n{formatted_liked_videos}")
#     return HttpResponse(f"Vidéos aimées :\n{formatted_liked_videos}")



    
    
def add_track_to_playlist(sp, user_id, playlist_id, track_uri):
    # Ajoutez la chanson à la playlist Spotify en utilisant Spotipy
    sp.user_playlist_add_tracks(user_id, playlist_id, [track_uri])

def add_song_to_spotify_playlist(request, video_title):
    # Obtenez le jeton d'accès OAuth pour Spotify
    spotify_access_token = request.COOKIES.get('spotify_token')
    # token = request.COOKIES.get('token')

    if spotify_access_token:
        sp = Spotify(auth=spotify_access_token)
        user_id = spotify_user_id(request)
        search_results = sp.search(q=video_title, type='track', limit=1)

        if search_results['tracks']['items']:
            track_uri = search_results['tracks']['items'][0]['uri']
            print('TRACK:', track_uri)
            playlist_id = create_spotify_playlist_1(request)
            print('playlist:', playlist_id)
            add_track_to_playlist(sp, user_id, playlist_id, track_uri)

            return HttpResponse("Chanson ajoutée à la playlist Spotify!")
        else:
            return HttpResponse("Impossible de trouver l'URI Spotify de la chanson.")
    else:
        return HttpResponse("Erreur d'authentification Spotify.")
    



# def sync_youtube_like_to_spotify(request):
#     playlist_id = create_spotify_playlist(request)
#     spotify_access_token = request.COOKIES.get('spotify_token')
#     if not spotify_access_token:
#         return HttpResponse("Erreur d'authentification Spotify.")

#     # Obtenez les vidéos aimées depuis YouTube
#     token = request.COOKIES.get('token')
#     liked_videos = get_youtube_liked(token)
#     for video in liked_videos:
#         video_title = video['snippet']['title']
#         add_song_to_spotify_playlist(request, video_title, playlist_id)

#     return HttpResponse("Vidéos aimées synchronisées avec la playlist Spotify!")

def send_email(request, objet='Salutation', message='Bonjour,\nUne playlist a été crée.\nCordialement', collaborators=['axel.boussari@gmail.com', 'audreyneomiemigan@gmail.com']):
    # Vérifier que collaborators est une liste ou un tuple
    create_spotify_playlist_1(request)
    print("In send-email collaborators type : ", type(collaborators))
    if not isinstance(collaborators, (list, tuple)):
        raise TypeError('La liste des collaborateurs doit être une liste ou un tuple')

    # Créer l'objet EmailMessage avec la liste des collaborateurs
    email = EmailMessage(
        subject=objet,
        body=message,
        to=collaborators
    )
    email.send()
    return HttpResponse('E-mail envoyé avec succès !')


def send_email2(request, video_title, objet='Salutation', message='Bonjour,\n Une nouvelle chanson a été ajouté à la playlist "Chansons écoutées".\nCordialement', collaborators=['axel.boussari@gmail.com', 'audreyneomiemigan@gmail.com']):
    # Vérifier que collaborators est une liste ou un tuple
    add_song_to_spotify_playlist(request, video_title)
    create_spotify_playlist_1(request)
    print("In send-email collaborators type : ", type(collaborators))
    if not isinstance(collaborators, (list, tuple)):
        raise TypeError('La liste des collaborateurs doit être une liste ou un tuple')

    # Créer l'objet EmailMessage avec la liste des collaborateurs
    email = EmailMessage(
        subject=objet,
        body=message,
        to=collaborators
    )
    email.send()
    return HttpResponse('E-mail envoyé avec succès !')

# Create your views here.
