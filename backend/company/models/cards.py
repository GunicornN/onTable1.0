from django.contrib.auth.models import User
from django.db import models
from .company import Company

from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    description = models.CharField(max_length=250,blank=True,null=True)
    available = models.BooleanField(default=1)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    slug = models.SlugField(max_length = 250, null = True, blank = True)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product)

    slug = models.SlugField(max_length = 250, null = True, blank = True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Card(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=200,blank=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category,related_name='categories',blank=True) #optionnal Field

    slug = models.SlugField(max_length = 250, null = True, blank = True)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Card, self).save(*args, **kwargs)

class Formula(models.Model):
    name = models.CharField(max_length=45)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(max_length = 250, null = True, blank = True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Formula, self).save(*args, **kwargs)

"""
class Category_Product(models.Model):
    order = models.IntegerField() #increment in forms
    obligatory = models.BooleanField(default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
"""
