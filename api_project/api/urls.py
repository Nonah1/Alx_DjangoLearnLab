from  django.urls import path, include
from api.views import BookListCreateAPIView, BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list'),
    path("books/", BookList.as_view()),

    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),  # This includes all routes registered with the router

]

