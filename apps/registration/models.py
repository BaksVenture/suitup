from django.db import models
from django.contrib.auth import models as models2
from clothes.models import Brand
import datetime

class User(models.Model):
    user = models.OneToOneField(models2.User)
    fname = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    subscriptions = models.ManyToManyField(Brand)
    
    def __unicode__(self):
        return str(self.user)
