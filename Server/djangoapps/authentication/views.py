from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from drf_yasg import openapi
from .renderers import UserRenderer


# Create your views here.
# Renderer est une composante responsable de l'affichage d'un contenu dans le navigateur

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)
        
class LoginAPIView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)