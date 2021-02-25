from django.db import models
from company.models import Company


import os 
class pictureCardManager(models.Manager):
    def get_cards_from_company(self,company,*args,**kwargs):
        """
        cards_from_company :
        Get the list of card of a company
        """
        queryset = super().get_queryset().filter(company=company,*args,**kwargs).values('name').distinct()
        return queryset

    def get_images_from_company_card(self,company,card_name,*args,**kwargs):
        """
        images_from_company_card :
        Get all images associated with a card 
        """
        queryset = super().get_queryset().filter(company=company,name=card_name,*args,**kwargs)
        return queryset


class pictureCard(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload_by = models.CharField(max_length=20,default='company')
    picture = models.FileField(upload_to='images/', blank=True)

    #Manager 
    objects = pictureCardManager()
    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return "{}_{}".format(self.name,self.company)

    def delete(self,*args,**kwargs):
        try:
            os.remove(self.picture.path)
        except FileNotFoundError as e:
            pass #lever une erreur ici 
        
        super().delete(*args, **kwargs)
#--------------------------------------------------
# TRASH
#--------------------------------------------------
class Document(models.Model):
    """
    This Model : bye bye
    PLEASE REMOVE THIS IF I FORGOT IT
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    document = models.FileField(upload_to='documents/',blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload_by = models.CharField(max_length=20,default='company')
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return "{}_{}".format(self.name,self.company)