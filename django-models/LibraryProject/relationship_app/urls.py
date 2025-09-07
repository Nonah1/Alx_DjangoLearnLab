from .views import list_books, LibraryDetailView, register
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    path("admin-view/", admin_view, name="admin_view"),
    path("librarian-view/", librarian_view, name="librarian_view"),
    path("member-view/", member_view, name="member_view"),
    path('books/', list_books, name='books'),
    path("", list_books, name="home"),   # 👈 root path points to list_books
    path('library_detail/<int:pk>', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('register/', register, name='register' ),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout') 
]