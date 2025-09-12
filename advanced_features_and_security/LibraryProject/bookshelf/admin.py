from .models import Book
from django.contrib import admin, CustomUser

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('title', 'publication_year')

admin.site.register(Book)
admin.site.register(CustomUser)
