from django.db import models
from company.models import Company

class QRCode(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='temp/', blank=True)

    class Meta:
        verbose_name = 'QRCode'
        verbose_name_plural = 'QRCodes'
