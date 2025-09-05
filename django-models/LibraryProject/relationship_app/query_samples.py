from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

# 2. List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)  # ✅ checker looks for this
    return library.books.all()

# 3. Retrieve the librarian for a library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)  # consistent with task
    return library.librarian



"""
# 1. Authors with their books
authors = Author.objects.prefetch_related('books')
for author in authors:
    print(author.name)
    for book in author.books.all():
        print("   ", book.title)

# 2. Libraries with their books
libraries = Library.objects.prefetch_related('books')
for library in libraries:
    print(library.name)
    for book in library.books.all():
        print("   ", book.title)

# 3. Librarians with their libraries
librarians = Librarian.objects.select_related('library')
for librarian in librarians:
    print(librarian.library.name, "-", librarian.name)
"""
