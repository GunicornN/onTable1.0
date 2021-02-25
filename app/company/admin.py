from django.contrib import admin
from company.models import Company, pictureCard, Category, Card, Product, Table, Cart, Type

admin.site.register(Category)
admin.site.register(Company)
admin.site.register(pictureCard)

admin.site.register(Card)
admin.site.register(Product)

admin.site.register(Table)

admin.site.register(Cart)
admin.site.register(Type)