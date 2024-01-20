from django.shortcuts import render
import json
import requests
from django.http import HttpResponse
from django.shortcuts import redirect

'''
authentification à trello
@trello_user_auth :  affiche une page ou on renseigne ses identifiants
                    redirige vers la fonction trello_user_token
@trello_user_token :  récupère le code et génère le token d'accès à l'API
                    stocke le token dans un cookie
'''
from requests_oauthlib import OAuth1

# Informations d'authentification Trello

trello_params = {
    'requestURL' : "https://trello.com/1/OAuthGetRequestToken",
    'accessURL' : "https://trello.com/1/OAuthGetAccessToken",
    'authorizeURL' : "https://trello.com/1/OAuthAuthorizeToken",
    'appName' : "Areact",
    'scope' : 'read,write', # account,boards,organizations',
    'expiration' : '1hour',
    'key' : "55f502e17f42d9f8b7040e114d3a24af", #api-key
    'secret' : "50d9ffaf60e40c9e884b33640ea24adba85dc46b209abfd59970f363c7ae2518", # api-secret
    'loginCallback' : "http://127.0.0.1:8000/trello-auth/", # lien de redirection
    'oauth_secrets' : {}, # Dictionnaire pour stocker temporairement les paires de token et tokenSecret
}
oauth = OAuth1(trello_params['key'], client_secret=trello_params['secret'], callback_uri=trello_params['loginCallback']) # Objet OAuth1 pour gérer l'authentification OAuth

def trello_user_auth(request):
    # Obtention du token de demande
    response = requests.post(trello_params['requestURL'], auth=oauth)
    oauth_token = response.text.split('&')[0].split('=')[1]
    oauth_secret = response.text.split('&')[1].split('=')[1]
    trello_params['oauth_secrets'][oauth_token] = oauth_secret

    # Redirection vers l'URL d'autorisation Trello avec le token
    authorize_url = f"{trello_params['authorizeURL']}?oauth_token={oauth_token}&name={trello_params['appName']}&scope={trello_params['scope']}&expiration={trello_params['expiration']}"
    return redirect(authorize_url)

# Vue pour l'URL de rappel après l'authentification
def trello_user_token(request):
    oauth_token = request.GET.get('oauth_token')
    oauth_secret = trello_params['oauth_secrets'].get(oauth_token)
    oauth_verifier = request.GET.get('oauth_verifier')

    # Obtention du token d'accès
    oauth = OAuth1(trello_params['key'], client_secret=trello_params['secret'], resource_owner_key=oauth_token,
                   resource_owner_secret=oauth_secret, verifier=oauth_verifier)
    response = requests.post(trello_params['accessURL'], auth=oauth)
    access_token = response.text.split('&')[0].split('=')[1]
    access_secret = response.text.split('&')[1].split('=')[1]

    # Mettre le token d'accès dans un cookie
    setCookie = HttpResponse('Cookie set!')
    setCookie.set_cookie('trello_token', access_token, max_age=3600)
    print(access_token)
    return setCookie
    # return HttpResponse(access_token)

'''
@create_trello_board    : Create board with trello api
params : nom du board
'''

def create_trello_board(request, name) :
    access_token = request.COOKIES.get('trello_token')
    print("Access token : ", access_token)

    # name = 'ProjectTest'
    url = "https://api.trello.com/1/boards/"

    query = {
    'name': name,
    'key': trello_params['key'],
    'token': access_token
    }

    response = requests.request(
    "POST",
    url,
    params=query
    )

    # print(response.text)
    response_json = response.json()
    #invite_member(request, collaborators, response_json)
    print(response_json)
    return (response_json)

'''
@invite_member  : Invité des membres sur le board de trello
params : la liste des membres à ajouter, les caractéristiques du board, les noms des membres
'''

def invite_member(request, collaborators, response_json, fullName) :
    access_token = request.COOKIES.get('trello_token')
    if 'id' in response_json:
        board_id = response_json['id']
        print("ID du tableau créé :", board_id)
        url = f"https://api.trello.com/1/boards/{board_id}/members"

        headers = {
        "Content-Type": "application/json"
        }
        for i in range(len(collaborators)) :
            query = {
            'email': collaborators[i],
            'key': trello_params['key'],
            'token': access_token
            }

            payload = json.dumps( {
            "fullName": fullName[i]
            } )

            response = requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            params=query
            )

            print(response.text)
        return ("Les invitations ont été bien envoyé.")
    else:
        return ("Erreur lors de la création du tableau :", response_json)

