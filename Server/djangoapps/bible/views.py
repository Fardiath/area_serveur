from django.shortcuts import render
from django.http import HttpResponse
import requests
from Twilio.views import *

def get_bible_verse(request):
    url = "https://labs.bible.org/api/?passage=random&type=json"
    try:
        response = requests.get(url)
        data = response.json()

        if data:
            book = data[0]['bookname']
            chapter = data[0]['chapter']
            verse = data[0]['verse']
            text = data[0]['text']
            passage = f"{book} {chapter}:{verse} - {text}"
            send_whatsapp_message(passage, '+22961133565')
            return HttpResponse(passage)
        else:
            return HttpResponse("Aucune donnée disponible.")
    except Exception as e:
        return HttpResponse(f"Erreur : {e}")