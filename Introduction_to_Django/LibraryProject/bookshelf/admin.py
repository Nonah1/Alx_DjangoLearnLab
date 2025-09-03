from django.contrib import admin
from bookshelf.models import Book

# Register your models here.
class BookAdmin(admin.ModeAdmin):
    list_display = ('title', 'author', 'published_year')
    search_fields = ('title', 'author')

admin.site.register(Book)
