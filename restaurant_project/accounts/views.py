from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import RegisterUserSerializer
from rest_framework import mixins

# Create your views here.

User = get_user_model()


class RegisterUserViewsets(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset= User.objects.all()
    serializer_class = RegisterUserSerializer
