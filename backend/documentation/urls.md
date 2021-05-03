# URLS 
Toutes les urls de l'API sont décrites ici. 
Vous trouverez plus d'informations sur les routes, la vue associée ainsi que le namespace

Comment accéder manuellement à celles-ci ? 
Grâce au package django_extensions dans INSTALLED_APPS.

Commande : 
` python manage.py show_urls `


# Company 
/company/       company.views.company.Company   company-list

/company/       rest_framework.routers.APIRootView      api-root

/company/<pk>/  company.views.company.Company   company-detail

/company/<pk>\.<format>/        company.views.company.Company   company-detail

/company/\.<format>/    company.views.company.Company   company-list

/company/\.<format>/    rest_framework.routers.APIRootView      api-root


# Company : Documents 
/company/document/      company.views.documents.Document        picturecard-list

/company/document/<pk>/ company.views.documents.Document        picturecard-detail


URL :/company/document/<pk>/delete_document/ 
Viewset : company.views.documents.Document        
Namespace : picturecard-delete-document


/company/document/<pk>/delete_document\.<format>/       company.views.documents.Document        picturecard-delete-document

/company/document/<pk>/upload_document/ company.views.documents.Document        picturecard-upload-document

/company/document/<pk>/upload_document\.<format>/       company.views.documents.Document        picturecard-upload-document

/company/document/<pk>\.<format>/       company.views.documents.Document        picturecard-detail

/company/document/test/ company.views.documents.Document        picturecard-test

/company/document/test\.<format>/       company.views.documents.Document        picturecard-test

/company/document\.<format>/    company.views.documents.Document        picturecard-list


# Allauth  

/rest-auth/login/       rest_auth.views.LoginView       rest_login

/rest-auth/logout/      rest_auth.views.LogoutView      rest_logout

/rest-auth/password/change/     rest_auth.views.PasswordChangeView      rest_password_change

/rest-auth/password/reset/      rest_auth.views.PasswordResetView       rest_password_reset

/rest-auth/password/reset/confirm/      rest_auth.views.PasswordResetConfirmView        rest_password_reset_confirm

/rest-auth/registration/        rest_auth.registration.views.RegisterView       rest_register

/rest-auth/registration/account-confirm-email/<key>/    django.views.generic.base.TemplateView  account_confirm_email

/rest-auth/registration/verify-email/   rest_auth.registration.views.VerifyEmailView    rest_verify_email

/rest-auth/user/        rest_auth.views.UserDetailsView rest_user_details

/users/api-token-auth/  rest_framework.authtoken.views.ObtainAuthToken  api_token_auth


# Tests 

/users/hello/   core.views.hello.HelloView      hello