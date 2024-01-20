from django.conf import settings
import requests
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.http import JsonResponse

def get_all_benin_cities(request):
    benin_cities = [
        'Abomey-Calavi', 'Allada', 'Aplahoué', 'Banikoara', 'Bassila', 'Bembèrèkè', 'Bohicon', 'Bori', 'Boukoumbé',
        'Comé', 'Cotonou', 'Cové', 'Dassa-Zoumè', 'Djougou', 'Dogbo-Tota', 'Kandi', 'Kérou', 'Kétou', 'Kouandé',
        'Lokossa', 'Malanville', 'Natitingou', 'Ndali', 'Nikki', 'Ouidah', 'Parakou', 'Pobè', 'Porto-Novo', 'Sakété',
        'Savalou', 'Ségbana', 'Tanguiéta', 'Tchaourou'
    ]

    # Convertir la liste en une seule chaîne de texte avec un saut de ligne entre chaque ville
    cities_text = '\n'.join(benin_cities)
    return HttpResponse(cities_text, content_type='text/plain; charset=utf-8')

# def get_weather(request):
#     api_key = settings.OPENWEATHERMAP_API_KEY
#     city = 'Cotonou'  # Remplacez par la ville de votre choix

#     # Appelez l'API OpenWeatherMap
#     api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
#     response = requests.get(api_url)
#     weather_data = {}
#     print('response:', response)

#     if response.status_code == 200:
#         weather_data = response.json()
#         temperature = weather_data['main']['temp']
#         humidity = weather_data['main']['humidity']
#         description = weather_data['weather'][0]['description']
        
#     return (weather_data)

def get_weather(request):
    api_key = settings.OPENWEATHERMAP_API_KEY
    city = request.GET.get('ville')  # Utilisez la valeur spécifiée dans la requête, pas de valeur par défaut

    if not city:
        return HttpResponse("Veuillez fournir le paramètre 'ville' dans la requête.", status=400)

    # Appelez l'API OpenWeatherMap
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(api_url)
    weather_data = {}
    print('response:', response)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']

    return HttpResponse(weather_data, content_type='application/json')

def send_email_weather(request, objet='Salutation', collaborators=['axel.boussari@gmail.com', 'audreyneomiemigan@gmail.com', 'abiboufardia@gmail.com']):
    # Vérifier que collaborators est une liste ou un tuple
    weather_data = get_weather(request)
    print('weather_data:', weather_data)

    if 'weather' in weather_data and len(weather_data['weather']) > 0:
        description = weather_data['weather'][0].get('description')
        if description == "few clouds":
            temperature = weather_data['main']['temp']
            message = f"Bonjour, le temps est {description} avec une température de {temperature}°C. Cordialement"
        else:
            message = f"Bonjour, le temps est différent de 'few clouds'. Cordialement"
    else:
        message = "Bonjour, les données météorologiques ne sont pas disponibles. Cordialement"

    print("Dans la fonction send_email, le type de collaborators est : ", type(collaborators))
    if not isinstance(collaborators, (list, tuple)):
        raise TypeError('La liste des collaborateurs doit être une liste ou un tuple')

    # Créer l'objet EmailMessage avec la liste des collaborateurs
    email = EmailMessage(
        subject=objet,
        body=message,
        to=collaborators
    )

    # Envoyer l'e-mail
    email.send()

    # Retourner la température dans la réponse HTTP
    return HttpResponse(f'E-mail envoyé avec succès !')



