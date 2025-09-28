from django.shortcuts import render
from rest_framework import generics, permissions
from api.models import Author, Book
from serializers import BookSerializer, AuthorSeriaizer
from django_filters import rest_framework
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

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

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and get token for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        response = self.client.post(reverse('api-token-auth'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Sample book
        self.book = Book.objects.create(
            title='Test Book',
            author='Author A',
            published_date='2025-01-01',
            isbn='1234567890123',
            pages=100
        )

    def test_create_book(self):
        data = {
            'title': 'New Book',
            'author': 'Author B',
            'published_date': '2025-02-01',
            'isbn': '9876543210123',
            'pages': 200
        }
        response = self.client.post(reverse('book-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(title='New Book').author, 'Author B')

    def test_retrieve_book(self):
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book(self):
        data = {'title': 'Updated Title'}
        response = self.client.patch(reverse('book-detail', kwargs={'pk': self.book.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

    def test_delete_book(self):
        response = self.client.delete(reverse('book-detail', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_permission_required(self):
        # Test without credentials
        client = APIClient()
        response = client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_books_by_author(self):
        Book.objects.create(title='Book2', author='Author B', published_date='2025-03-01', isbn='1112223334445', pages=150)
        response = self.client.get(reverse('book-list') + '?author=Author B')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Author B')

    def test_search_books_by_title(self):
        response = self.client.get(reverse('book-list') + '?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any('Test' in book['title'] for book in response.data))

    def test_order_books_by_pages(self):
        Book.objects.create(title='Book3', author='Author C', published_date='2025-04-01', isbn='5556667778889', pages=50)
        response = self.client.get(reverse('book-list') + '?ordering=pages')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pages_list = [book['pages'] for book in response.data]
        self.assertEqual(pages_list, sorted(pages_list))
