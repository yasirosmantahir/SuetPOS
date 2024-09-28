from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializer import CombinedSerializer

class CombinedCreateView(generics.CreateAPIView):
    serializer_class = CombinedSerializer