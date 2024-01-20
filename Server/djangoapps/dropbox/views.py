from django.shortcuts import render
import requests
# Create your views here.
import dropbox


def upload_picture(request) :
    # Mettez vos clés d'API Dropbox ici
    access_token = "VOTRE_ACCESS_TOKEN_DROPBOX"

    # URL de la photo à télécharger
    photo_url = "https://example.com/photo.jpg"

    # Chemin de destination sur Dropbox où vous souhaitez enregistrer la photo
    destination_path = "/chemin/sur/dropbox/photo.jpg"

    # Initialisation du client Dropbox
    client = dropbox.Dropbox(access_token)

    # Téléchargement de la photo à partir de l'URL et enregistrement sur Dropbox
    response = client.files_save_url(destination_path, photo_url)

    # Vérification du statut du téléchargement
    if response:
        print("La photo a été téléchargée avec succès sur Dropbox.")
    else:
        print("Erreur lors du téléchargement de la photo sur Dropbox.")