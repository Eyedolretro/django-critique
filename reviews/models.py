from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # homogène avec Ticket

    def __str__(self):
        return f"{self.user.username} - {self.rating}/5"

    @property
    def classname(self):
        return self.__class__.__name__

class UserFollows(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followed_by', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Response(models.Model):
    review = models.ForeignKey(Review, related_name="responses", on_delete=models.CASCADE)
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Article de {self.author.username} ({self.created_at})"
