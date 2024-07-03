from typing import Any
from django import forms
from .models import Borrowing
from django.contrib import messages

class  BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = []