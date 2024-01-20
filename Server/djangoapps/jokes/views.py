from django.shortcuts import render
import requests
from django.http import HttpResponse
from Twilio.views import *

def random_jokes(request) :    
    # Envoyer une requête GET à l'API pour récupérer une blague aléatoire
    response = requests.get("https://v2.jokeapi.dev/joke/Any")
    print('response = ', response)
    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        # Extraire les données de la réponse au format JSON
        joke_data = response.json()
        print('joke_data : ', joke_data)
        # Récupérer la blague et l'afficher
        if joke_data["type"] == 'single' :
            joke = joke_data["joke"]
        else :
            joke_setup = joke_data["setup"]
            joke_del = joke_data["delivery"]
            joke = f"{joke_setup}\nResponse: {joke_del}"
        send_whatsapp_message(joke, '+22961133565')
        return HttpResponse('Message send successfuly!')
    else:
        return HttpResponse("Erreur lors de la récupération de la blague.")
