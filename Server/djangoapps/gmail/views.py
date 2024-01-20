from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import HttpResponse

'''
@send_email:    Utilisation du server smtp pour l'envoi du mail à partir de gmail 
params: oject, message, destinataires
'''


def send_email(objet='Salutation', message='Bonjour,\nBienvenue mes cheres amis. Heureuse année.\nCordialement', collaborators=['neomie.migan@epitech.eu', 'audreyneomiemigan@gmail.com']):
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

