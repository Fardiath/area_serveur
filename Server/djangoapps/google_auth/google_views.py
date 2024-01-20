from google_auth_oauthlib.flow import InstalledAppFlow
from django.shortcuts import redirect
from django.http import HttpResponse
import requests


def google_authentification(request):
    flow = InstalledAppFlow.from_client_secrets_file(
        './client_secret.json',  # Chemin vers votre fichier client_secret.json
        scopes=[
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
            ],
    )
    flow.redirect_uri = 'http://13.48.177.31:8080/google/callback/'
    print("redirect:", flow.redirect_uri)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
    )
    print('authorization:', authorization_url)
    return redirect(authorization_url)


def google_authentification_callback(request):
    # if 'oauth_state' not in request.session or 'state' not in request.GET or request.session['oauth_state'] != request.GET['state']:
    #     print('CODE')
    #     return HttpResponse('error_page')
    flow = InstalledAppFlow.from_client_secrets_file(
        './client_secret.json',
         scopes=[
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
            ],
    )
    flow.redirect_uri = 'http://localhost:8080/google/callback/'
    
    return HttpResponse('Bienvenue sur Google!.')
