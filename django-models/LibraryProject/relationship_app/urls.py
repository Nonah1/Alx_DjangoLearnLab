from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    path('books/', list_books, name='books'),
    path("", list_books, name="home"),   # 👈 root path points to list_books
    path('library_detail/<int:pk>', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout') 
]