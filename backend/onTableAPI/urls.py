from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#Home Page
from home import views

from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
     url(r'^$',views.homePage_view,name="homePage"),
     url(r'^searchCompany/(?P<search>[-\w]+)/$',views.searchCompany,name="searchCompany"),
     url(r'^searchCompany/$',views.searchCompany,name="searchCompany"),
     url (r'^company_presentation/(?P<pk>[0-9]+)/$',views.company_presentation_view,name="companyPresentation"),

     url(r'^CGU/$',views.CGU_view,name="CGU"),
     url(r'^privacyPolicy/$',views.privacy_policy_view,name="privacyPolicy"),

     path(r'company/',include('company_manager.urls'),name="companySide"),
     path(r'orders/',include('orders.urls'),name="ordersSide"),
     path('accounts/', include('allauth.urls')),

     #trad
     url(r'^i18n/', include('django.conf.urls.i18n')),

     #admin
     path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'home.views.view_404'
handler500 = 'home.views.view_500'
