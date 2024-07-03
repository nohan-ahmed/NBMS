from django.contrib import admin
from .models import Book, Review
# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ['id', 'title','author', 'price',]
    list_filter = ['id', 'title','author', 'price', ]
    search_fields = ['id', 'title','author', 'price']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'book','user', 'rating',]
    list_filter = ['id', 'book','user', 'rating','created_at']
    search_fields = ['id', 'book','user', 'rating',]