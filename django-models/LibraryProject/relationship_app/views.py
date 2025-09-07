from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library, Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test

# Create your views here
# Role checkers
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"

def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"

def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"

def list_books(request):
    #Displays list
    books = Book.objects.all()    
    context = {"books": books}
    return render(request, 'relationship_app/list_books.html', context)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {"form": form} )


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = "library"




    



    

       








