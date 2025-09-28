from django.shortcuts import render
from rest_framework import generics, permissions
from api.models import Author, Book
from serializers import BookSerializer, AuthorSeriaizer
from django_filters import rest_framework

# Create your views here.
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# ✅ List all books (read-only for anyone)
class BookListView(generics.ListAPIView):
    """
    Retrieves a list of all books.
    Read-only: accessible to any user.
    Supports filtering, searching, and ordering (see Part 2).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # anyone can read

    # ✅ Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering by exact field values
    filterset_fields = ['title', 'author', 'publication_year']

    # Searching (case-insensitive contains)
    search_fields = ['title', 'author__name']

    # Ordering
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering

# ✅ Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single book by its ID.
    Read-only: accessible to any user.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ✅ Create a new book (restricted to authenticated users)
class BookCreateView(generics.CreateAPIView):
    """
    Creates a new Book.
    Only authenticated users can create.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# ✅ Update an existing book (restricted to authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing Book instance.
    Only authenticated users can update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# ✅ Delete a book (restricted to authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes a Book instance.
    Only authenticated users can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
