#Import company model
from company.models import Company
#groups
from django.contrib.auth.models import (AbstractUser, BaseUserManager, Group,
                                        User)
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name,last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        # Create staff user
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,first_name=username)

        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user       


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

    objects = MyUserManager() # Manager 

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
