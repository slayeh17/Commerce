from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_core = models.CharField(max_length=100)

    def __str__(self):
        return self.category_core

class Listing(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    bid = models.FloatField(default=0.0)
    img_url = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    is_available = models.BooleanField(default=True)
    length = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")

    def __str__(self):
        return self.title

class Comment(models.Model):
    pass