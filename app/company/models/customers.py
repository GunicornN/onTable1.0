from django.db import models
from company.models import Company
from phonenumber_field.modelfields import PhoneNumberField

class Customer(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    writed_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=254)
    phoneNumber = PhoneNumberField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'

    def __str__(self):
        return "{} for {}".format(self.writed_at,self.company)