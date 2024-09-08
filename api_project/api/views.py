from django.shortcuts import render
from api.models import Book
from .serializers import BookSerializer
from rest.framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticated]
  serializer_class = BookSerializer
  model = Book
  queryset = Book.objects.all()

