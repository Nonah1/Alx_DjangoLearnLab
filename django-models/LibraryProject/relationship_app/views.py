from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from relationship_app.models import Library, Book

# Create your views here
def list_books(request):
    #Displays list
    books = Book.objects.all()    
    context = {"books": books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = "library"
    

       










