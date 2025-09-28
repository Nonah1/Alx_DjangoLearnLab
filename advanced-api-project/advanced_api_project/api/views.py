from django.shortcuts import render
from rest_framework import generics
from api.models import Author, Book
from serializers import BookSerializer, AuthorSeriaizer

# Create your views here.
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer