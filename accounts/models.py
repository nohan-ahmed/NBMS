from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomManager
# Create your models here.

class User(AbstractUser):
    profile_pic = models.ImageField( upload_to='', default='default profile avatar.png')
    email = models.EmailField(unique=True, max_length=254)
    phone = models.CharField(max_length=11)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=1200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomManager()

    def __str__(self) -> str:
        return super().__str__()


class Account(models.Model):
    user = models.OneToOneField(to=User, related_name='account', on_delete = models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    address = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    country = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f'{self.id}'
    
    def deposite(self, amount):
        print(self)
        self.balance += amount
        self.save()