from django import forms
from .models import Review
from .models import Ticket


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


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']


class ArticleForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Écris ton article ici...'}),
        label='Contenu de l’article'
    )

