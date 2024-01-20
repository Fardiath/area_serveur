from django.shortcuts import render
from django.http import HttpResponse
import requests
import random
import json
from newsapi.views import find_article 

def random_dog_uri(request) :
    # Faire la requête à l'API Dog API pour obtenir une image aléatoire de chien
    response = requests.get("https://api.thedogapi.com/v1/images/search")

    # Vérifier que la requête s'est effectuée avec succès
    if response.status_code == 200:
        # Extraire l'URL de l'image de la réponse JSON
        data = json.loads(response.text)
        image_url = data[0]["url"]
        
        # Faire quelque chose avec l'URL de l'image, par exemple, l'afficher
        return HttpResponse(f"Voici une image aléatoire de chien : {image_url}")
    else:
        # Gérer les erreurs de requête
        return HttpResponse("Une erreur s'est produite lors de la requête à l'API Dog API.")
    
def random_dogs_uri(request) :
    # Nombre d'images souhaitées
    num_images = 20

    # Liste pour stocker les URLs des images
    image_urls = []

    # Effectuer la requête pour num_images
    response = requests.get(f"https://api.thecatapi.com/v1/images/search?limit={num_images}")
    data = json.loads(response.text)

    for uri in data :
        image_url = uri["url"]
        image_urls.append(image_url)

    return HttpResponse(f'dog uri has been sucessfuly upload! : {image_urls}')


def random_breed_name(request) :
    response = requests.get("https://dog.ceo/api/breeds/list/all")
    data = response.json()

    if response.status_code == 200 and data["status"] == "success":
        breeds = list(data["message"].keys())
        random_breed = random.choice(breeds)
        topic = 'Dog Breed : ' + random_breed
        article = find_article(topic)
        if data["articles"] != [] :
            random_breed_name(request)
        return (article)
    else:
        return ("Erreur lors de la requête API")