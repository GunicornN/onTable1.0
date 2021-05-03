from django.http import HttpResponse
from django.shortcuts import redirect, render

#Import company model
from company.models import Company

#groups
from django.contrib.auth.models import Group

#Import exceptions
from django.core.exceptions import ObjectDoesNotExist

def profil_completed(view_func):
    def wrapper_func(request, *args,**kwargs):
        return render(request,'account/no_authorized.html')
        current_user = request.user
        try:
            iCompany = Company.objects.get(id=current_user.company_id)
        except ObjectDoesNotExist:
            return render(request, 'errors/noCompleted.html')
        #Check if profile is full completed
        if not iCompany.check_if_profil_completed():
            return render(request, 'errors/noCompleted.html')

        return view_func(request,*args,**kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()
                for g in group:
                    if g.name in allowed_roles :
                        return view_func(request,*args,**kwargs)
                else :
                    return render(request,'account/no_authorized.html')
            else :
                return redirect('CSSettings')
        return wrapper_func
    return decorator

def allowed_only_subscription1():
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            users_in_group = Group.objects.get(name="subscription1").user_set.all()
            if request.user in users_in_group:
                return view_func(request,*args,**kwargs)
            else :
                return render(request, 'errors/noCompleted.html')
        return wrapper_func
    return decorator

