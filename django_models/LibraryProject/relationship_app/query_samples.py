from models import Author, Book, Library, Librarian

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
