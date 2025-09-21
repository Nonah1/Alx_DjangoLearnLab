from rest_framework import generics
from api.models import Book
from .serializers import BookSerializer
from django.shortcuts import render

# Create your views here.
class BookListCreateAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer