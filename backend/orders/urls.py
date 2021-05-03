from django.conf.urls import url
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    re_path(r'^$',views.connexion_view,name="OSConnexion"),
    re_path(r'connexion/',views.connexion_view,name="OSConnexion"),
    re_path(r'^(?P<company_code>[-\w]+)/$',views.company_home,name="OSHome"),
    re_path(r'^customerInfo/(?P<company_code>[-\w]+)/$',views.CustomerInfo,name="OSCustomerInfo"),
    re_path(r'^(?P<company_code>[-\w]+)/(?P<document_name>.*)/$',views.company_cards,name="OSSeeDocument"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'orders.views.view_404'
handler500 = 'orders.views.view_500'
