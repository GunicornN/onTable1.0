## company/urls.py
"""
onTablePro : Company : URL Configuration

"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

"""
CS : Company Side
ES : Employee Side
"""
urlpatterns = [

    url(r'^$',views.homePage_view,name="CSHome"),
    url(r'^home/$',views.homePage_view,name="CSHome"),

    url(r'^orders/$',views.orders_view,name="CSOrders"),
    url(r'^settings/$',views.settings_view,name="CSSettings"),

    url(r'^deleteDocument/(?P<document_name>.*)/$',views.delete_upload,name="CSDeleteDocument"),
    url(r'^seeDocument/(?P<document_name>.*)/$',views.view_document,name="CSViewDocument"),
    url(r'^uploadDocument/$',views.model_form_upload,name="CSUploadDocument"),

    url(r'^QRCodes/$',views.manage_qrcodes_view,name="CSQRCodes"),
    url(r'^payment/$',views.payment_view,name="CSPayment"),

    url(r'^deleteAccount/$',views.delete_account_view,name="DeleteAccount"),

    #Customers Infos
    url(r'^customers/$',views.manage_customer_infos_view,name="CSCustomersInfos"),
    url(r'^deleteCustomers/(?P<customer_id>\d+)/$',views.delete_customer_infos,name="CSDeleteCustomersInfos"),

    # [ADMIN] Online orders
    url(r'^onlineOrders/$',views.manage_online_orders_view,name="CSOnlineOrders"),
    url(r'^deleteOnlineOrders/(?P<online_order_id>\d+)/$',views.delete_online_orders,name="CSDeleteOnlineOrders"),

    #Search Tests
    # url(r'^search/$', views.search, name='search'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


"""
handler404 = 'company.views.view_404'
handler500 = 'company.views.view_500'
"""