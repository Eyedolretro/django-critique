from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'headline': 'Titre',
            'body': 'Critique',
            'rating': 'Note (1 à 5)',
        }
