#onTableAPI/urls.py
from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path(r'users/',include('core.urls'),name="users"), #<-- remove this
    path(r'api/',include('company.urls'),name="company"),

    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]
