from django import forms
from .models import Review
from .models import Ticket
from django.contrib.auth.models import User
from .models import Response


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



class FollowUserForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur à suivre")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Utilisateur introuvable.")


class FollowForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur à suivre", max_length=150)




class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Votre droit de réponse...'}),
        }

