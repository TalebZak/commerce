from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Product(models.Model):
    class Category(models.TextChoices):
        FURNITURE = 'FU', _('Furniture')
        CLOTHING = 'CL', _('Clothing')
        ENTERTAINMENT = 'EN', _('Entertainment'),
        OTHER = 'OTH', _('Other')

    product_type = models.CharField(max_length=3,
                                    choices=Category.choices, default='OTH')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=78)
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    date_posted = models.DateField(auto_now=True)
    description = models.TextField(default="No description for this listing")
    #image = models.ImageField()

    def __str__(self):
        return f"{self.name}"
