from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    first_name = models.TextField(max_length=30)
    last_name = models.TextField(max_length=30)
    followers = models.ManyToManyField(
        'self', related_name='following', symmetrical=False)
    image = models.FileField(upload_to='network/images')
    # Introduction of user
    # Target language
    # Learning language
    # Contacts 
    def __str__(self):
        return self.username
    
    # def save(self, *args, **kwargs):
    #     # Check if the user is trying to follow themselves
    #     if self in self.following.all():
    #         raise ValidationError("You cannot follow yourself.")

    #     super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    def __str__(self):
        return f"{self.title} from {self.author.username}"


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    def __str__(self):
        return f"{self.content} from {self.author.username}. Parent: {self.parent}"

class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')
    def __str__(self):
        return f"{self.user.username} on {self.post.id}."
    class Meta:
        unique_together = ["user", "post"]

