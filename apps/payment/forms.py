# -*- coding: utf-8 -*-
from django import forms

class OrderForm(forms.Form):
    address = forms.CharField(
        label='Адрес',
    )
    phone = forms.CharField(
        label='Контактный телефон',
    )
    
    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

