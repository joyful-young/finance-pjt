from django import forms

from .models import DepositProducts, DepositOptions

class DepositProductsForm(forms.ModelForm):

    class Meta:
        model = DepositProducts
        fields = '__all__'


class DepositOptionsForm(forms.ModelForm):

    class Meta:
        model = DepositOptions
        fields = '__all__'
