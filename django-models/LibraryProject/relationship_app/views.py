from django.shortcuts import render
from django.views.generic import ListView
from .models import Book

# Create your views here
def list_books(request):
    #Displays list
    books = Book.objects.all()
    
    context = {"books": books}

    return render(request, 'book/book_list.html', context)

class LibraryView(ListView):
    model = Book
    template_name = 'books/library_detail.html'

    books = Book.objects.all()

       










