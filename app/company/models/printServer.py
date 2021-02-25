from django.db import models
from .tables import Table, Cart, Cart_Items

class PrintStatus(models.Model):
    # cart id referenced
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)

    # status of printing
    # 0 = first print
    # 1 = printed
    # 2 = error
    # 3 = make duplicata (aka re-print)
    status = models.IntegerField(default=0)

    # date and time of creation in db
    created_on = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"PrintStatus: {self.status} (Cart {self.cart_id.id} for {self.cart_id.person_name})"