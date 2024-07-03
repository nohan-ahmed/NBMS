from django.db import models
from accounts.models import Account
from categories.models import Category
from django.db.models import Avg
# Create your models here.
from django.db import models
from django.db.models import Avg

class Book(models.Model):
    image = models.ImageField(upload_to='books/media')
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    page = models.IntegerField()
    category = models.ManyToManyField(to=Category, related_name='book')
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    slug = models.SlugField(max_length=250, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.title}'

    def average_rating(self):
        # Aggregate the average rating of the related reviews
        average = self.reviews.aggregate(Avg('rating'))['rating__avg']
        # Return the average rating rounded to one decimal place or 0 if there are no reviews
        return round(average, 1) if average is not None else 0.0

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(Account, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.book.title} by {self.user.user.username}'
