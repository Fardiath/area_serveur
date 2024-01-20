from django.shortcuts import render
from django.http import HttpResponse
import praw
import requests
from opentrivia.views import find_question
from newsapi.views import random_topic


# Créez une instance de la classe Reddit en vous authentifiant avec votre client ID et votre secret ID


reddit = praw.Reddit(
    client_id='b99uawPd2VzZprnX99yA3A',
    client_secret='ppJvCThnHuvkDHXdwvUUDTQdY1_lWg',
    user_agent='Areact/1.0',
    username='Neomie05',
    password='areact12345'
)

def article_publication(request) :
    subreddit = reddit.subreddit('Areact')
    article = random_topic(request)
    print("article = ", article)
    title = article.split("Titre : ")[1].split("\n")[0]
    description = article.split("Description : ")[1].split("\nURL")[0]
    url = article.split("URL : ")[1]
    subreddit.submit(title, selftext=f'Description: {description}.Url = {url}')
    return HttpResponse("Article is submit successfuly")

def ask_question(request) :
    subreddit = reddit.subreddit('AreaTest')

    question_list = find_question(request)
    question = question_list[0]
    print("question : ", question)
    title = question["category"]
    body = question['question']
    submission = subreddit.submit(title, selftext=body)

    if submission:
        return HttpResponse("Votre question a été soumise avec succès à la page d'accueil de Reddit !")
    else:
        return HttpResponse("Une erreur s'est produite lors de la soumission de votre question.")
