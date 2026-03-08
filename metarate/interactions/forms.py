
from django import forms

from interactions.models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['title', 'text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Поделитесь своим мнением…',
            }),
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 10,
            }),
        }

