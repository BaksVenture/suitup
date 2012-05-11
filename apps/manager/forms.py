from django.forms import ModelForm
from clothes.models import Clothes

class ClothesForm(ModelForm):
  class Meta:
    model = Clothes
