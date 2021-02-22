from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from company.models import Company
from django.db import models

#groups
from django.contrib.auth.models import Group

#Import company model
from company.models import Company

class CustomUser(AbstractUser):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('email address', unique=True)
    # the foreign key field is optional for CustomUser until
    # the CustomUser  hasn't company
    company = models.ForeignKey(Company,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def setGroup(self):
        company_group = Group.objects.get(name='companyGroup') 
        company_group.user_set.add(self)

    def hasCompany(self):
        return self.company is not None

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'


#-----------------------------------------------
#           World Model 
#-----------------------------------------------
from django.contrib.gis.db import models

class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name