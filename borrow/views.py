from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Borrowing
from books.models import Book
from .forms import BorrowForm
from django.contrib import messages
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import send_email

# Create views here.
class BorrowView(LoginRequiredMixin, CreateView):
    model = Borrowing
    form_class = BorrowForm
    template_name = './borrow/borrow.html'
    success_url = reverse_lazy('profile')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        if pk:
            context['book'] = get_object_or_404(Book, pk=pk)
        else:
            context['book'] = None
        return context

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        account = self.request.user.account
        book = get_object_or_404(Book, pk=pk) if pk else None

        if book and account.balance < book.price:
            messages.info(self.request, f"You don't have enough balance to borrow this book! Your current balance is ${account.balance}")
            return self.form_invalid(form)
        else:
            if book:
                account.balance -= book.price
                account.save()
            borrowing = form.save(commit=False)
            borrowing.account = account
            borrowing.book = book
            borrowing.save()
            messages.success(self.request, message=f"Successfully borrowed {book}")
            send_email(self.request.user, borrowing, "successfully borrowed a book", './borrow/send_borrowed_email.html')
            return super().form_valid(form)
        

class ReturnView(LoginRequiredMixin, UpdateView):
    model = Borrowing
    fields = []  # No fields to display in the form
    template_name = 'borrow/return_confirmation.html'  # Optional: confirmation template
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        borrow = form.save(commit=False)
        borrow.is_return = True
        borrow.return_date = timezone.now()
        borrow.save()
        self.request.user.account.balance += borrow.book.price
        self.request.user.account.save()
        send_email(self.request.user, borrow, "successfully return a book", './borrow/send_return_email.html')

        return super().form_valid(form)
