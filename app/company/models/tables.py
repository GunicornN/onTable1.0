from django.contrib.auth.models import User
from django.db import models
from .company import Company


from .cards import Product, Formula
"""
Add __str__ for name
This file contains : 
- Table Model 
- Cart Model 
- Cart_Items Model 
- 
"""


class Table(models.Model):
    table_no = models.IntegerField()
    table_code = models.CharField(max_length=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now_add=True, blank=True) #added

    def __str__(self):
        return f"Table:{self.table_no}"

    #ADD Table_Code Generator 

class Cart(models.Model):
    person_name = models.CharField(max_length=45)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=45)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    #updateOn = models.DateTimeField(auto_now_add=True, blank=True)
    paid_on = models.DateTimeField(auto_now_add=True, blank=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

class Cart_Items(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    items = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True) #Can be null
    formulas = models.ForeignKey(Formula, on_delete=models.CASCADE,blank=True, null=True) #Can be null
