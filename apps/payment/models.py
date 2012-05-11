from django.db import models
from clothes.models import Clothes
from django.contrib.auth.models import User


# Create your models here.

class Order(models.Model):
    products = models.ManyToManyField(Clothes)
    buyer = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    amount = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    payment_system = models.CharField(max_length=3)
    create_date = models.DateTimeField()
    payment_date = models.DateTimeField(null=True, blank=True)
    
    def __unicode__(self):
        return str(self.id)
    
class OrderStatus(models.Model):
    order_no = models.ForeignKey(Order)
    date = models.DateTimeField()
    mess = models.TextField()
    
    def __unicode__(self):
        return str(self.order_no)
