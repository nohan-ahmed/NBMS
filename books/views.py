from typing import Any
from django.shortcuts import render,redirect
from django.views.generic import DetailView
from .models import Book, Review
from .forms import ReviewForm
from django.contrib import messages
from django.urls import reverse
from borrow.models import Borrowing
# Create your views here.


class DetailBook(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = './books/book_details.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        book = self.get_object()
        context['average_rating'] = book.average_rating()
        context['reviews'] = book.reviews
        return context
    
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        book = self.get_object()
        
        # Check if the user has borrowed the book
        user_account = request.user.account
        has_borrowed = Borrowing.objects.filter(account=user_account, book=book, is_return=False).exists()
        
        if has_borrowed:
            if form.is_valid():
                form.instance.user = user_account
                form.instance.book = book
                form.save()
                messages.success(request, "Your review has been submitted successfully.")
            else:
                messages.error(request, "There was an error with your review submission.")
        else:
            messages.info(request, "Please borrow the book before you can give a review.")
        
        return redirect(reverse('detail_book', kwargs={'slug':book.slug,'id': book.id}))
