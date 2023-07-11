from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_core = models.CharField(max_length=100)

    def __str__(self):
        return self.category_core

class Bid(models.Model):
    bid = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")

    def __str__(self):
        return f"{self.user}: {self.bid}"

class Listing(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_bid")
    img_url = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    is_available = models.BooleanField(default=True)
    length = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    watchlist = models.ManyToManyField(User, related_name="user_watchlist")

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment_text = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_comment")
    
    def __str__(self):
        return f"{self.author} commented on {self.listing}."

