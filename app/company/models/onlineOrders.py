from django.db import models
from company.models import Company

class OnlineOrders(models.Model):
    """
    Online Orders : To Buy Qr-Codes, NFC puces, ...
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    description = models.CharField(max_length=255, help_text="Une demande particulière ? Donnez-nous plus de détails.")
    custom_QRCodes = models.BooleanField()
    number_for_choice1  = models.PositiveSmallIntegerField(blank=True, default=0)
    number_for_choice2  = models.PositiveSmallIntegerField(blank=True, default=0)

    address1 = models.CharField( max_length=200)
    city = models.CharField(max_length=64, default="")
    zip_code = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Commande en ligne'
        verbose_name_plural = 'Commandes en ligne'

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"OrderFor{self.company}"
