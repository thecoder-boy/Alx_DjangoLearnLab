from .views import BookListApiView
from django.urls import path

urlpatterns = [
  path('books/', BookListApiView.as_view()),
]