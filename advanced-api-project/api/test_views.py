# api/test_views.py
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book
from django.urls import reverse

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass123')

        # Use Django test client (session-based) for authentication
        self.client = APIClient()
        login_successful = self.client.login(username='testuser', password='testpass123')
        assert login_successful, "User login failed in test setup!"

        # Create a sample book
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

