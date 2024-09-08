from .views import BookListApiView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('books', BookListApiView)

urlpatterns = [
  # path('books/', BookListApiView.as_view()),
  path('books-endpoint/', include(router.urls))
]