"""
Create permission groups
Create permissions (read only) to models for a set of groups

thx to radtek  : https://stackoverflow.com/a/53733693/11092569


just run : manage.py create_groups
"""

import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


GROUPS = ['companyGroup', 'employeeGroup','subscription1','administratorGroup']
MODELS = ['CompanyUser', 'EmployeeUser']
PERMISSIONS = ['view', ]



class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    name = 'Can {} {}'.format(permission, model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)

        print("Created default group and permissions.")
