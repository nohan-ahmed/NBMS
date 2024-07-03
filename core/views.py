from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from books.models import Book
from categories.models import Category
from django.shortcuts import get_object_or_404
# Create your views here.

class HomeView(ListView):
    model=Book
    context_object_name = 'books'
    template_name='index.html'
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug', None)
        if slug:
            cat = get_object_or_404(Category, slug=slug)
            queryset = queryset.filter(category=cat)
        return queryset