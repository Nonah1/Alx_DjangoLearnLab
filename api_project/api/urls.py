from  django.urls import path, include
from api.views import BookListCreateAPIView

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list'),
    path("books/", BookList.as_view())

]
