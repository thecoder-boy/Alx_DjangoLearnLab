from django.shortcuts import render
from api.models import Book
from api.serializers import BookSerializer
from rest.framework.generics import ListApiView
# Create your views here.

class BookListApiView(ListApiView):
  serializer_class = BookSerializer
  model = Book
  queryset = Book.objects.all()

