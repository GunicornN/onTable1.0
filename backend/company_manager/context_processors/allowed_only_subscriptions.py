
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group

"""
This function return the name of the company, to display it into the nav bar

"""
def display_for_susbcribers1(request):
    """
    try:
        users_in_group = Group.objects.get(name="subscription1").user_set.all()
        if request.user in users_in_group:
            return {'isSusbcribers1': True}

    except ObjectDoesNotExist:
        return {'isSusbcribers1': False}
    """
    return {'isSusbcribers1': True}
