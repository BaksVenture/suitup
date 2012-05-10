from django.contrib import admin
from clothes.models import ClothesCategory, \
    Brand, Clothes, ClientCategory
    

admin.site.register(ClothesCategory)
admin.site.register(ClientCategory)
admin.site.register(Clothes)
admin.site.register(Brand)
