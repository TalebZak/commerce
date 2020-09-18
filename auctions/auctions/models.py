from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save


class User(AbstractUser):
    pass


class Category(models.TextChoices):
    FURNITURE = 'FU', _('Furniture')
    CLOTHING = 'CL', _('Clothing')
    ENTERTAINMENT = 'EN', _('Entertainment')
    OTHER = 'OTH', _('Other')


class Product(models.Model):
    """The model of my product, includes a slug, price, a description and owner"""
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=True)
    product_type = models.CharField(max_length=3,
                                    choices=Category.choices)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=78)
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    date_posted = models.DateField(auto_now=True)
    description = models.TextField(default="No description for this listing")
    image = models.ImageField(upload_to='images/%Y/%m/%D/', null=True, blank=True, default='images/no-image.png')

    def __str__(self):
        return f"{self.name}"

    # returns the url of the product
    def get_url_path(self):
        return f'{self.slug}'

'''Creates a slug field, by assigning a none value first
   , takes results from the filter method, 
   then does a recursive call to make the slug of the product'''
def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug:
        slug = new_slug
    result = Product.objects.filter(slug=slug).order_by('-id')#order by serves as a way to take the element that was recently added
    exists = result.exists()
    if exists:#if a product with the same name exists, we will rely on the recent element
        new_slug = "%s-%s" % (slug, result.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug#return the slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Product)


class Watchlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    addition_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.product.name}"


class Bid(models.Model):
    value = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"current bid: {self.value}$"

    def __le__(self, other):#operator '<=' overloading for ease of comparison between bids
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
