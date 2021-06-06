from django.contrib.auth.models import User
from django.db import models
from .company import Company

from django.db import models
from .cards import Product, Formula

# slug generator 
from django.utils.text import slugify

CHOICES_PRINT_STATUS = [
    (0,'First print'),
    (1,'Printed'),
    (2,'Error'),
    (3,'Duplicata')
]

class Table(models.Model):
    table_no = models.IntegerField()
    table_code = models.CharField(max_length=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now_add=True, blank=True) #added

    def __str__(self):
        return f"Table:{self.table_no}"

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
    table = models.ForeignKey(Table,related_name='cart',on_delete=models.CASCADE)

    slug = models.SlugField(max_length = 250, null = True, blank = True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.person_name)
        super(Cart, self).save(*args, **kwargs)

    def set_total_amount(self):
        price = 0.0
        cart_items = self.cart_items.all()
        formulas = []
        for cart_item in carts_items:
            if cart_item.formulas :
                formulas.append(carts_items)
            else :
                product_price = cart_item.product.price
                price += product_price

        for formula in formulas:
            pass
            #formula.__categories

class Cart_Items(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    vat = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)

    cart = models.ForeignKey(Cart, related_name='items',on_delete=models.CASCADE)
    items = models.ForeignKey(Product, related_name='products',on_delete=models.CASCADE,blank=True, null=True) #Can be null   # JSON 
    formulas = models.ForeignKey(Formula, on_delete=models.CASCADE,blank=True, null=True) #Can be null  # JSON 

class PrintStatus(models.Model):
    # cart id referenced
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)

    # status of printing
    # 0 = first print
    # 1 = printed
    # 2 = error
    # 3 = make duplicata (aka re-print)
    # 100 = Commande finalisée

    status = models.IntegerField(choices=CHOICES_PRINT_STATUS,default=0)

    # date and time of creation in db
    created_on = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"PrintStatus: {self.status} (Cart {self.cart_id.id} for {self.cart_id.person_name})"
