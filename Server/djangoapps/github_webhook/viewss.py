import json
import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.mail import EmailMessage


def hello(request):
    return HttpResponse('<h1>Hello Django!</h1>')

'''
@send_email:    Utilisation du server smtp pour l'envoi du mail à partir de gmail 
params: oject, message, destinataires
'''

def send_email(objet, message, collaborators):
    # Vérifier que collaborators est une liste ou un tuple
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


'''
Créate repo with github API
@get_github_auth :  affiche une page ou on renseigne ses identifiants
                    redirige vers la fonction github_callback
@github_callback :  récupère le code et génère le token d'accès à l'API
                    stocke le token dans un cookie
@create_github_repo  :  créer le référentiel et ajoute les collaborateurs
params : nom du repo, description, nom d'utilisateurs et email des vcollaborateurs, optionel(Readme, Private/Public, Gitignore)
'''

def get_github_auth(request):

    # Url de redirection
    redirect_uri = 'http://127.0.0.1:8080/github_callback/'

    # Rediriger l'utilisateur vers l'URL d'autorisation GitHub
    authorization_url = f'https://github.com/login/oauth/authorize?client_id=34e7ff1ed326df4692fa&redirect_uri={redirect_uri}&scope=repo'
    return redirect(authorization_url)

def github_callback(request):
    # Récupérer le code d'autorisation de la requête
    code = request.GET.get('code')
    redirect_uri = 'http://127.0.0.1:8080/github_callback/'

    # Effectuer une demande POST pour échanger le code contre un jeton d'accès
    token_url = 'https://github.com/login/oauth/access_token'
    payload = {
        'client_id': "34e7ff1ed326df4692fa",
        'client_secret': '845ff90e57a19563b9e997e7741687dc42fe59ad',
        'code': code,
        'redirect_uri': redirect_uri
    }
    headers = {'Accept': 'application/json'}
    response = requests.post(token_url, data=payload, headers=headers)

    # Extraire le jeton d'accès de la réponse JSON
    access_token = response.json().get('access_token')

    # Mettre le token d'accès dans un cookie
    setCookie = HttpResponse('Authentification réussie')
    setCookie.set_cookie('github_token', access_token, max_age=3600)
    print(access_token)
    return setCookie

# Créer un repo github
def create_github_repo(request):

    # Extraire le jeton d'accès de cookies
    access_token = request.COOKIES.get('github_token')
    collaborateurs = ['Hamidboussari', 'mandra002', 'Tekboy']
    collaborateurs_mail = ['hamid.boussari@epitech.eu', 'edem.metinhoue@epitech.eu', 'fredtossou3@gmail.com']

    repoName = 'RepoTest' 
    description = 'Description du repo' 
    # Utiliser le jeton d'accès pour créer un nouveau référentiel
    repo_data = {
        'name': repoName, # nom du repo ou du référentiel
        'description': description, # description du repo ou du référentiel
        'auto_init': True, # Création d'un Readme
        'private': True, # True pour le repo est privé et False pour un repo public
        'collaborators': collaborateurs, # liste des collaborateurs
        'gitignore_template': 'Python' # Les éléments à perndre en compte dans le gitignore
    }
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    create_repo_response = requests.post('https://api.github.com/user/repos', json=repo_data, headers=headers)

    # Vérifier le statut de la requête de création de référentiel
    if create_repo_response.status_code == 201:
        response_json = create_trello_board(request, repoName)
        if collaborateurs is not None :
            add_collaborators(headers=headers, repoName=repoName, collaborateurs=collaborateurs)
            invite_member(request, collaborateurs_mail, response_json, collaborateurs)
        return HttpResponse(f"Le référentiel a été créer avec succès : {repoName}", status=create_repo_response.status_code)
    else:
        return HttpResponse(f"Échec de la création du référentiel : {create_repo_response.text}", status=create_repo_response.status_code)

def add_collaborators(headers, repoName, collaborateurs) :
    i = 0
    # Recupèration du owner
    get_owner = requests.get("https://api.github.com/user", headers=headers)
    if get_owner.status_code == 200:
        user_data = get_owner.json()
        owner = user_data["login"]
        print(f"Nom d'utilisateur GitHub : {owner}")
    else:
        return HttpResponse(f"Échec de la récupération des informations de l'utilisateur. Statut de la réponse : {owner.status_code}")

    while i in range(len(collaborateurs)):
        # URL de l'API pour ajouter un collaborateur à un référentiel
        url = f"https://api.github.com/repos/{owner}/{repoName}/collaborators/{collaborateurs[i]}"
        data = {
            "permission": 'push'
        }
        response = requests.put(url, headers=headers, json=data)

        if response.status_code == 201 :
            print("Le collaborateur a été ajouté avec succès", response.status_code)
        else :
            print("Le collaborateur n'a pas été ajouté avec succès", response.status_code)
        i = i + 1



'''
Créer un issues
@create_issues  : créer un issue et l'assigne à des un collaborateur
params: le nom d'utilisateurs de l'admin, le nom du référentiel,
        le titre et la description de la tâche, le nom du collaborateur à qui la tâche va être assigné,
        mail du collaborateur à qui la tâche va être assigner
'''

def create_issues(request) :

    # Informations d'authentification
    token = "votre_token_d_acces"
    token = request.COOKIES.get('github_token')

    # Nom du référentiel GitHub
    repository_owner = "Neomie05" # le nom d'utilisateurs de l'admin
    repository_name = "RepoTest" # le nom du référentiel

    # URL de l'API GitHub pour créer une carte
    api_url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/issues"

    # Headers de la requête
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}",
    }

    # Titre et corps de la tâche
    task_title = "Test de mon application pour le projet django"
    task_body = "Description_de_la_tache pour le projet test"

    # Nom d'utilisateur et email du collaborateur à assigner
    assignee_username = "mandra002"
    mail = ['edem.metinhoue@epitech.eu']

    # Corps de la requête
    data = {
        "title": task_title,
        "body": task_body,
        "assignees": [assignee_username]
    }

    # Envoi de la requête
    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    # Vérification du statut de la requête
    if response.status_code == 201:
        objet = "Creation d'un issues"
        collaborators = mail
        print("Collaborators type : ", type(collaborators))
        message = f"Bonjour {assignee_username},\nTu as été mise sur une tâche par {repository_owner} sur le projet {repository_name}.\nCordialement" # le message
        send_email(objet, message, collaborators)
        return HttpResponse(f"Tâche créée et assignée à {assignee_username} avec succès!")
    else:
        return HttpResponse(f"Une erreur s'est produite lors de la création de la tâche. Code d'erreur :{response.status_code}. Message d'erreur : {response.text}")

'''
@create_branch : céer une branche sur un repo github
params :  nom du propriétaire du repo, nom du repo, nom de la branche, nom de la branche de base,
          nom d'utilisateur, mail des collaborateurs
'''

def create_branch(request) :
    # Informations d'authentification
    token = "votre_token_github"
    token = request.COOKIES.get('github_token')
    repo_owner = "Neomie05" # nom du propriétaire du repo
    repo_name = "RepoTest" # 

    # Données pour créer la branche
    branch_name = "NewBranche"
    base_branch = "main"

    # URL de l'API GitHub pour créer une branche
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs"

    # Paramètres de l'en-tête de la requête
    headers = {
        "Authorization": f"Token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Récupérer le commit de la branche de base
    base_branch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/heads/{base_branch}"
    response = requests.get(base_branch_url, headers=headers)

    # Vérifier la réponse de la requête
    if response.status_code == 200:
        response_json = json.loads(response.text)

        # Vérifier si la clé 'object' est présente dans la réponse JSON
        if "object" in response_json and "sha" in response_json["object"]:
            commit_sha = response_json["object"]["sha"]

            # Créer les données JSON pour créer la nouvelle branche
            data = {
                "ref": f"refs/heads/{branch_name}",
                "sha": commit_sha
            }

            # Effectuer la requête POST pour créer la branche
            response = requests.post(url, headers=headers, json=data)

            # Vérifier la réponse de la requête
            if response.status_code == 201:
                username = "Neomie05"
                collaborator = ['hamid.boussari@epitech.eu', 'edem.metinhoue@epitech.eu', 'fredtossou3@gmail.com']
                if collaborator is not None :
                    objet = "Creation d'une nouvelle branche"
                    message = f"Bonjour,\nVotre collaborateur {username} a créé une nouvelle branche {branch_name} sur le référentiel {repo_name}.\nCordialement"
                    send_email(objet, message, collaborator)
                return HttpResponse("La branche a été créée avec succès.")
            else:
                return HttpResponse(f"Une erreur s'est produite lors de la création de la branche. Code de statut : {response.status_code}. Réponse : {response.text}")
        else:
            return HttpResponse("La clé 'object' n'a pas été trouvée dans la réponse JSON.")
    else:
        return HttpResponse(f"Une erreur s'est produite lors de la récupération du commit de la branche de base. Code de statut : {response.status_code}. Réponse : {response.text}")



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
    'loginCallback' : "http://13.48.177.31:8080/trello-auth/", # lien de redirection
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
        return HttpResponse("Les invitations ont été bien envoyé.")
    else:
        return HttpResponse("Erreur lors de la création du tableau :", response_json)
