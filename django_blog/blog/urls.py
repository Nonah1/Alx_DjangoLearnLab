# blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Registration & profile
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),

    # Login / Logout (Django's built-in views with custom templates)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    # --- Post CRUD URLs ---
    path('', views.PostListView.as_view(), name='post-list'),                     # / -> list of posts
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),   # /post/1/
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),        # /post/new/
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),  # /post/1/update/
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),  # /post/1/delete/

    path('post/<int:post_pk>/comments/new/', views.comment_create, name='comment-create'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),


]
 
