from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    return HttpResponse("Book creation page")

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return HttpResponse(f"Editing book: {book.title}")

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return HttpResponse("Book deleted")


# Create your views here.
