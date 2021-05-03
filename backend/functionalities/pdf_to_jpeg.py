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
"""
from celery import shared_tasks

app = Celery('functionalities', broker=BROKER_URL)

@shared_tasks()
def add(x, y):
    return x + y
@shared_tasks()
"""



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
                pages[page].save('media/images/'+name, 'JPEG')

                with transaction.atomic():
                    p = pictureCard(name=nameOfCard,company=company,picture=name,pdf_linked_to=document)
                    p.save()


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
            pages[page].save('media/images/'+name, 'JPEG')

            with transaction.atomic():
                p = pictureCard(name=nameOfCard,company=company,picture=name,pdf_linked_to=document)
                p.save()


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
                pages[page].save('media/images/'+name, 'JPEG')
                with transaction.atomic():
                    p = pictureCard(name=nameOfCard,company=company,picture=name,pdf_linked_to=document)
                    p.save()
    return True
