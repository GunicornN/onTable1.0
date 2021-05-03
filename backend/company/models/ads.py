from django.db import models
from company.models import Company


class Advertisement(models.Model):
    picture = models.ImageField(upload_to='advertisements/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    ttl = models.DateTimeField()
    companies = models.ManyToManyField(Company)
    view = models.IntegerField(default=0)

    def __str__(self):
        return self.uploaded_at
