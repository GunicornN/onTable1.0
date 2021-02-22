from django.db import models
from company.models import Company

class Printer(models.Model):
    company = models.ForeignKey(Company)
    created_on = models.DateTimeField() #On a besoin du time 
    
