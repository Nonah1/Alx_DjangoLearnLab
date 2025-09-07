from .views import list_books, LibraryView
from django.urls import path

urlpatterns = [
    path('books/', list_books, name='books'),
    path("", list_books, name="home"),   # 👈 root path points to list_books
    path('library_detail/<int:pk>', LibraryView.as_view(), name='library_detail') 
]