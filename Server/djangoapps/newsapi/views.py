from django.shortcuts import render
from django.http import HttpResponse
import requests


def random_topic(request) :
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnnamespace": "0",  # Limiter aux articles principaux
        "rnlimit": "1"  # Nombre d'articles aléatoires à récupérer
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Vérifier si la requête a réussi
    if response.status_code == 200 and "query" in data:
        #articles = [article["title"] for article in data["query"]["random"]]
        # print("data : ", data)
        title = data["query"]["random"][0]["title"] 
        data = find_article(title)
        if data["articles"] != [] :
            random_topic(request)
        
        return HttpResponse(data)
    else:
        return HttpResponse("Erreur lors de la requête API")

def find_article(topic) :
    # Remplacez "YOUR_API_KEY" par votre propre clé d'API
    api_key = "8055d3637d154713ad32d1d43f310975"

    # Remplacez "YOUR_TOPIC" par le sujet pour lequel vous souhaitez obtenir des articles
    # topic = "santé"

    # Effectuer la requête à l'API News
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    print('data_articles : ', data)
    article = data["articles"][0]
    return(article)

    # # Vérifier si la requête a réussi
    # if response.status_code == 200 and data["status"] == "ok" and data["articles"] != []:
    #     # Récupérer le premier article
    #     article = data["articles"][0]
    #     title = article["title"]
    #     description = article["description"]
    #     url = article["url"]
        
    #     # Utilisez les données de l'article comme vous le souhaitez
    #     return (f"Titre : {title}\nDescription : {description}\nURL : {url}")
    # else:
    #     return("Erreur")
