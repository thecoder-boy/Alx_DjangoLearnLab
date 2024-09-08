from django.shortcuts import render
from api.models import Book
from .serializers import BookSerializer
from rest.framework import generics
# Create your views here.

class BookListApiView(generics.ListAPIView):
  serializer_class = BookSerializer
  model = Book
  queryset = Book.objects.all()

