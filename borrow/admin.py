from django.contrib import admin
from .models import Borrowing
# Register your models here.
class BorrowAdmin(admin.ModelAdmin):
    list_display = ['id', 'account','book','is_return','borrow_date','return_date']
admin.site.register(Borrowing, BorrowAdmin)