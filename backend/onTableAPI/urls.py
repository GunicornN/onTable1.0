#onTableAPI/urls.py
from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # ADMIN DOCS 
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    # API 
    path(r'api/',include('company.urls'),name="api"),

    # REST-AUTH/ 
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    # Company Manager 
    url(r'company_manager/',include('company_manager.urls'),name="company_manager"),

    # Allauth Authentification 
    path('accounts/', include('allauth.urls')),
]
