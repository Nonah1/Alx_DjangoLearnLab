from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.LibraryView.as_view(), name='books'),
    path('library_detail/', views.book_list, name='library_detail')
]