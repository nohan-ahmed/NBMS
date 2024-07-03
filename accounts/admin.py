# yourapp/admin.py
from django.contrib import admin
from .models import User, Account

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'birth_date', 'is_staff', 'is_active']
    list_filter = ['username', 'email', 'phone', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'phone']

admin.site.register(User, UserAdmin)

class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'address', 'city', 'country']
    search_fields = ['id', 'user', 'country']

admin.site.register(Account, AccountAdmin)
