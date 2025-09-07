from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import ListView, DetailView
from .models import Library

# Create your views here
def list_books(request):
    #Displays list
    books = Book.objects.all()
    
    context = {"books": books}

    return render(request, 'relationship_app/list_books.html', context)

class LibraryView(ListView):
    model = Book
    template_name = 'relationship_app/library_detail.html'

    books = Book.objects.all()

       










