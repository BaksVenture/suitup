from django.forms import ModelForm
from clothes.models import Clothes, Brand

class ClothesForm(ModelForm):
  class Meta:
    model = Clothes

class BrandForm(ModelForm):
  class Meta:
    model = Brand
