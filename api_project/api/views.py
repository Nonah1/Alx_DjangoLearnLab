from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import Book
from .serializers import BookSerializer
from django.shortcuts import render

# Create your views here.
class BookListCreateAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # must be logged in


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Safe methods = GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

