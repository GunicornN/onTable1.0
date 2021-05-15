# OnTableAPI/company/views/qrcodes.py

import django_filters
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from company.models import Company, pictureCard
#from .serializers import CompanySerializers, CategoriesSerializers, CategorySerializers, PictureCardSerializers
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet
