# -*- coding: utf-8 -*-
from django import forms

class OrderForm(forms.Form):
    full_name = forms.CharField(
        label = 'Фамилия Имя Отчество'
    )
    address = forms.CharField(
        label='Адрес',
    )
    phone = forms.CharField(
        label='Контактный телефон',
    )
    email = forms.EmailField(
        label='E-mail',
        required=False,
    )
    
    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

