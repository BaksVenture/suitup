from django.contrib import admin
from clothes.models import ClothesCategory, Brand, Clothes

admin.site.register(ClothesCategory)
admin.site.register(Clothes)
admin.site.register(Brand)
