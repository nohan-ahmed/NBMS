from django.db import models
from accounts.models import Account
from books.models import Book
# Create your models here.
class Borrowing(models.Model):
    account = models.ForeignKey(to=Account, related_name='borrow_history', on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, related_name='borrowed_books', on_delete=models.CASCADE)
    is_return = models.BooleanField(default=False)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    def __str__(self) -> str:
        return f"{self.id}"