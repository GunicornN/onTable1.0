#celery 
from celery.decorators import task
from celery import shared_task

#Modules for img:       ??????
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onTablePro.settings")

from company.models import (
    Company,
    pictureCard,
    Document,
)

#Import transactions and errors
from django.db import transaction
from pdf2image import convert_from_path
import tempfile

from PyPDF2 import PdfFileReader

from django.conf import settings

from django.core.files.storage import FileSystemStorage

# importing the requests library for google map call 
import requests 


"""
https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/


"""

#/////////////////////////////////////////////////
# PLEASE REMOVE THIS AFTER UPDATE 
#/////////////////////////////////////////////////

@shared_task()
def convert_all_pdf_from_company(companyCode):
    """
    convert all pdfs of a company
    """
    company = Company.objects.get(company_code=companyCode)
    lsPdfs = Document.objects.filter(company=company)
    with tempfile.TemporaryDirectory() as path:
        for document in lsPdfs :
            nameOfCard = Document.objects.get(company_code=companyCode,id=document.id).name
            pages = convert_from_path(document.document.path)
            for page in range(0,len(pages)) :
                name = str((document.document.name.split('/')[-1]).split('.')[-2]) + str(page) + '.jpeg'
                pages[page].save(os.path.join(settings.MEDIA_ROOT,'images/{}'.format(name)), 'JPEG')

                with transaction.atomic():
                    p = pictureCard(name=nameOfCard,company=company,picture=name,pdf_linked_to=document)
                    p.save()

@shared_task()
def convert_from_company_pdf(nameOfCard,companyCode):
    """
    Convert one pdf to img:
    e.g. : documentRelais.pdf -> documentRelais0.jpeg, documentRelais1.jpeg
    """
    company = Company.objects.get(company_code=companyCode)
    document = Document.objects.get(company=company,name=nameOfCard)

    with tempfile.TemporaryDirectory() as path:
        pages = convert_from_path(document.document.path, fmt='jpeg',output_folder=path)
        for page in range(0,len(pages)) :
            name = str((document.document.name.split('/')[-1]).split('.')[-2]) + str(page) + '.jpeg'
            pages[page].save(os.path.join(settings.MEDIA_ROOT,'images/{}'.format(name)), 'JPEG')

            with transaction.atomic():
                p = pictureCard(name=nameOfCard,company=company,picture=name,pdf_linked_to=document)
                p.save()

@shared_task()
def convert_and_check_company_pdf(nameOfCard,companyCode,files_upload_count):
    """
    Convert one pdf to img:
    e.g. : documentRelais.pdf -> documentRelais0.jpeg, documentRelais1.jpeg
    """
    company = Company.objects.get(company_code=companyCode)
    document = Document.objects.get(company=company,name=nameOfCard)

    pages = PdfFileReader(open(document.document.path,'rb'))
    pages_count = pages.getNumPages()
    if pages_count > files_upload_count:
        with tempfile.TemporaryDirectory() as path:
            pages = convert_from_path(document.document.path, fmt='jpeg',output_folder=path)
            for page in range(files_upload_count,pages_count) :
                name = str((document.document.name.split('/')[-1]).split('.')[-2]) + str(page) + '.jpeg'
                pages[page].save(os.path.join(settings.MEDIA_ROOT,'images/{}'.format(name)), 'JPEG')
                with transaction.atomic():
                    p = pictureCard(name=nameOfCard,company=company,picture=name,pdf_linked_to=document)
                    p.save()
    return True

#/////////////////////////////////////////////////
# END REMOVE THIS AFTER UPDATE 
#/////////////////////////////////////////////////

@shared_task()
def convert_pdf_to_jpeg(pathFile,companyCode,cardName,upload_by):
    """
    Convert one pdf to images:
    e.g. : documentRelais.pdf -> documentRelais0.jpeg, documentRelais1.jpeg
    """
    print("--------")
    print("convert_pdf_to_jpeg ")
    company = Company.objects.get(company_code=companyCode)
    print("2")
    with tempfile.TemporaryDirectory() as path:
        pages = convert_from_path(pathFile, fmt='jpeg',output_folder=path)
        for page in range(0,len(pages)) :
            name = 'images/'+ str((pathFile.split('/')[-1]).split('.')[-2]) + str(page) + '.jpeg'
            pages[page].save(os.path.join(settings.MEDIA_ROOT,name), 'JPEG')

            with transaction.atomic():
                #Create images
                p = pictureCard(name=cardName,company=company,picture=name,upload_by=upload_by)
                p.picture.name = name
                p.save()
    print("3")
    # It remove the pdf after generating images
    os.remove(pathFile)



