from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Library, Book, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from .forms import BookForm   # you'll need a form for Book



# Create your views here

# Add Book
@permission_required("relationship_app.can_add_book")
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("books")
    else:
        form = BookForm()
    return render(request, "relationship_app/add_book.html", {"form": form})


# Edit Book
@permission_required("relationship_app.can_change_book")
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("books")
    else:
        form = BookForm(instance=book)
    return render(request, "relationship_app/edit_book.html", {"form": form})


# Delete Book
@permission_required("relationship_app.can_delete_book")
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("books")
    return render(request, "relationship_app/delete_book.html", {"book": book})
# Role checkers
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"

def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"

def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"

# --- Role-based views ---
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

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




    



    

       








