from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('books/', views.LibraryView.as_view(), name='books'),
    path('library_detail/', views.book_list, name='library_detail')
]