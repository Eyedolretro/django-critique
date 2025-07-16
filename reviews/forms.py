from django import forms
from .models import Review
from .models import Ticket
from django.contrib.auth.models import User
from .models import Response
from .models import Article


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']  # ✅ Les vrais noms de champs de ton modèle
        labels = {
            'content': 'Votre critique',
            'rating': 'Note (sur 5)',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 5}),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }



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

