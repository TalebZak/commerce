from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Category(models.TextChoices):
    FURNITURE = 'FU', _('Furniture')
    CLOTHING = 'CL', _('Clothing')
    ENTERTAINMENT = 'EN', _('Entertainment')
    OTHER = 'OTH', _('Other')


class Product(models.Model):
    status = models.BooleanField(default=True)
    product_type = models.CharField(max_length=3,
                                    choices=Category.choices, default='OTH')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=78)
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    date_posted = models.DateField(auto_now=True)
    description = models.TextField(default="No description for this listing")
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Watchlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    addition_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.product.name}"


class Bid(models.Model):
    value = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    listing = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"current bid: {self.value}$"

    def __le__(self, other):
        if other:
            return self.value <= other.value
        return False


class Comment(models.Model):
    subject = models.CharField(max_length=64)
    body = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    posting_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.body}"
