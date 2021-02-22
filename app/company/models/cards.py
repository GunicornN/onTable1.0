from django.contrib.auth.models import User
from django.db import models
from .company import Company

from django.db.models.signals import pre_save
#from company.utils import unique_slug_generator

class Product(models.Model):
    name = models.CharField(max_length=45)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    description = models.CharField(max_length=250)
    available = models.BooleanField(default=1)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=200,blank=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category,related_name='categories')

    """
    slug = models.SlugField(
        default='',
        editable=False,
        unique=True,
        max_length=55
    )
    """

    def __str__(self):
        return self.name
"""
class Category_Product(models.Model):
    order = models.IntegerField() #increment in forms
    obligatory = models.BooleanField(default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
"""
class Formula(models.Model):
    name = models.CharField(max_length=45)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(
        default='',
        editable=False,
        unique=True,
        max_length=50
    )


"""
Why ? 
def slug_save(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.name,instance.slug)

pre_save.connect(slug_save,sender=Products)
pre_save.connect(slug_save,sender=Categories)
pre_save.connect(slug_save,sender=Formula)
pre_save.connect(slug_save,sender=Cards)
"""