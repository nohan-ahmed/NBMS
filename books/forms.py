from django import forms
from .models import Review
from .containt import CHOICES
from .models import Book, Review
class ReviewForm(forms.ModelForm):
    Rating = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = Review
        fields = ['Rating', 'comment']
        
    def save(self, commit=True):
        review = super().save(commit=False)
        review.rating = int(self.cleaned_data['Rating'])
        if commit:
            review.save()
        return review