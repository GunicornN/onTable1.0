from django.contrib.auth.models import User
from django.db import models

#for the geocoding 
import requests

#for code generator 
from baseconv import base36
# ----------------------------------------------------------------
#  Import of module for phone numbers
# Documentation : https://github.com/stefanfoulis/django-phonenumber-field
# ----------------------------------------------------------------
from phonenumber_field.modelfields import PhoneNumberField

from django.conf import settings

# Slug 
from django.utils.text import slugify

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
# ----------------------------------------------------------------
# Type Of Company  
# ----------------------------------------------------------------

"""
Ici j'ai changé un nom : Category -> Type 
Peut avoir des bugs 
"""

class TypeManager(models.Manager):
    def get_company_from_category(self,category,*args,**kwargs):
        """
        Type_from_company :
        Get the list of company categories 
        """
        #queryset = super().get_queryset().filter(name=category,*args,**kwargs).values('name')
        queryset = Company.objects.filter(company__categories=category,*args,**kwargs)
        return queryset

class Type(models.Model):
    """
    Type of Restaurant like a Gastronomic, Fast-Food, ...
    """
    name = models.CharField("Catégorie de Restaurant",max_length=100) 

    #Manager 
    objects = TypeManager()

    def __str__(self):
        return self.name
# ----------------------------------------------------------------
# COMPANY 
# ----------------------------------------------------------------

class CompanyManager(models.Manager):
    def get_nearby(self,latitude,longitude,*args,**kwargs):
        """
        get_nearby :
        Get the nearest restaurants with location arguments
        Can return only 5 Restaurants, then 5 others if page argument is passed

        Help :
        https://stackoverflow.com/questions/37603454/calculating-near-gps-coordinates-in-django
        
        """
        #queryset = Company.objects.filter(company__categories=category,*args,**kwargs)
        Company.objects.filter( location=Distance('position', user_location)
            ).order_by('distance').first()
        #----------------------------
        # Make THIS 
        #----------------------------
        return queryset



class Company(models.Model):
    """
    Model of Company
    A company has:

     - A user (to be changed in order to accept multiple users
     who will be servers (we can change it after))

     - A unique identifier for the company (code_company)

     - A name corresponding to the name of the Company

     - An email

     - Date added

     - Telephone number

     - Subscribe to newsletter subscription


    See the MLD to have more informations

    """
    name = models.CharField("Nom de l'entreprise",max_length=200)

    address1 = models.CharField("addresse", max_length=200)
    address2 = models.CharField("seconde addresse", max_length=200, blank=True)

    city = models.CharField("ville", max_length=64, default="")
    country = models.CharField("pays", max_length=64, default="France")
    zip_code = models.IntegerField("code postal", default=0)

    _location = models.PointField(geography=True, default=Point(0.0, 0.0))
    #Company code used to define the restaurant in the QRCode
    company_code = models.CharField(max_length=4,blank=True,default='')

    current_ad = models.SmallIntegerField(default=0)

    profilPicture = models.FileField(upload_to='profils/', blank=True)

    types = models.ManyToManyField(Type)

    slug = models.SlugField(max_length=40)

    #Manager 
    objects = CompanyManager()

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


    def __str__(self):
        return self.name

    def get_location(self):
        """
        Property getter for location
        """
        return [self._location.x,self._location.y]

    def set_location(self, value):
        """
        Property setter for location
        """
        self._location = value

    location = property(get_location, set_location)

    def save(self, *args, **kwargs):
        if self.location == GEOSGeometry(Point(0,0),srid=4326) :
            geocoding = self.get_geocoding_from_address(
                self.address1,
            self.city,self.country,
            self.zip_code)
            self.location = GEOSGeometry(Point(geocoding[0],geocoding[1]),srid=4326)
        if not self.slug :
            self.slug = slugify(self.name[:30])+'-'+slugify(self.zip_code)
        if self.id and not self.company_code :
            self.set_company_code()
        super(Company, self).save(*args, **kwargs)

    def check_if_profil_completed(self):
        attributs = vars(self)
        for attribut in attributs :
            try:
                if attribut == '':
                    return False
            except Exception :
                raise
        return True

    def get_geocoding_from_address(self,*args,**kwargs):
        """
        arguments : company, then the address
        what does this fct do?
        - initalyse correct data for the request
        - get Geocoding of the address 
        - get correct datas from this request 
        - return lat and long for the company instance
        """
        address = ''
        url = 'https://maps.googleapis.com/maps/api/geocode/json'

        for arg in args :
            address += str(arg).replace(' ','+')

        data = {
            'address':address,
            'key':settings.GOOGLE_MAP_API_KEY
        } 

        request = requests.get(url = url, params = data) 
        response = request.json()
        if response['status'] == 'OK':
            latitude = response['results'][0]['geometry']['location']['lat'] 
            longitude = response['results'][0]['geometry']['location']['lng']
            return [longitude,latitude]
        else : 
            return [0,0]

    def set_company_code(self):
        """
        Property that generate a code for the company, used to unique code

        max number of companies : (35^4)/2 = 1 500 624/2  = 750 312

        ]0000 ; 750 312[ -> contains all the values with 4 characters

        *2 is just for the guys of will try to "hack" de system and connect to other
        companies

        base used = 35

        fct :
        nbr : id of company
        (2*nbr)[base 10] -> (nbr*2)[base 36]
        """        
        nbr = base36.encode((2*self.id))
        while len(nbr) <  4 :
            nbr = str(nbr) +  'Z'
        company_code = nbr.upper()

        self.company_code = company_code
        self.save()
