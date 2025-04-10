from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PostCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Post Categories"

class Post(models.Model):
    CATEGORIES = [
        ("Thought", "thought"),
        ("News", "News"),
        ("Tweet", "Tweet"),
        ("Instagram Post", "Instagram Post"),
        ("General", "General"),
    ]
    title = models.CharField(max_length=75)
    category = models.CharField(max_length=100, choices=CATEGORIES, blank=True, null=True, default="General")
    post_category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Post category")
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default="fallback.png", blank=True)
    html_file = models.FileField(upload_to='html_uploads/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.title
    