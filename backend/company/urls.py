from django.urls import path, include
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token


from rest_framework.routers import Route
from company import views

from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()


router.register(r'companies', views.CompanyReadViewSet,basename='company')
router.register(r'companies/(?P<company_slug>[-\w]+)/documents', views.DocumentViewSet,basename='documents')
router.register(r'companies/(?P<company_slug>[-\w]+)/cards', views.CardsViewSet,basename='cards')
router.register(r'companies/(?P<company_slug>[-\w]+)/products', views.ProductsViewSet,basename='products')
router.register(r'companies/(?P<company_slug>[-\w]+)/tables', views.TablesViewSet,basename='tables')
router.register(r'companies/(?P<company_slug>[-\w]+)/carts', views.CartsViewSet,basename='carts')
#router.register(r'customer', views.Document,basename='document')

urlpatterns = [
    path('', include(router.urls)),
    path('user/token/',views.CompanyOfUser)
]

