from relationship_app import views
from django.urls import path

urlpatterns = [
    path('books/', views.list_books, name='books'),
    path("", views.list_books, name="home"),   # 👈 root path points to list_books
    path('library_detail/<int:pk>', views.LibraryView.as_view(), name='library_detail') 
]