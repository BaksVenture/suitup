#-*- coding:utf-8 -*-
import os
from django.db import models
from clothes import settings as ns
from suituptools.string import slugify
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

def slugify_filename(filename):
    t = filename.split('.')
    name = slugify("".join(t[:-1]))
    ext = slugify(t[-1])
    filename = ".".join((name, ext,))
    return filename

class ClothesCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'Тип одежды'
        verbose_name_plural = 'Типы одежды'

    def __unicode__(self):
        return self.name
        
class ClientCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'Категория клиента'
        verbose_name_plural = 'Категории клиента'

    def __unicode__(self):
        return self.name
        
class Brand(models.Model):
    def logo_image_folder(self, filename):
        return os.path.join('uploads', 'brand', 'logo', \
            slugify(self.name), slugify_filename(filename))
            
    def background_image_folder(self, filename):
        return os.path.join('uploads', 'brand', 'background', \
            slugify(self.name), slugify_filename(filename))
            
    def border_image_folder(self, filename):
        return os.path.join('uploads', 'brand', 'border', \
            slugify(self.name), slugify_filename(filename))
    
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to = logo_image_folder, \
            default = ns.DEFAULT_BRANDLOGO_PATH)
            
    client_categories = models.ManyToManyField(ClientCategory)

    background = models.ImageField(upload_to = background_image_folder, \
            default = ns.DEFAULT_BRANDBACK_PATH)
            
    border_image = models.ImageField(upload_to = border_image_folder, \
            default = ns.DEFAULT_BRANDBORDER_PATH)
            
    manager = models.ForeignKey(User)
    colors = models.TextField()
    contacts = models.TextField()
    
    class Meta:
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'

    def __unicode__(self):
        return self.name
    
class Clothes(models.Model):
    def dress_image_folder(self, filename):
        t = filename.split('.')
        ext = slugify(t[-1])
        filename = ".".join((slugify(unicode(self.brand) + self.dress_id), ext,))
        return os.path.join('uploads', 'clothes', filename)

    dress_id = models.CharField(max_length=50)
    dress_img = models.ImageField(upload_to = dress_image_folder)
    price = models.IntegerField()
    sale_percent = models.IntegerField()
    brand = models.ForeignKey(Brand)
    dress_category = models.ForeignKey(ClothesCategory)
    
    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Одежда'

    def __unicode__(self):
        return self.dress_id
        
    
