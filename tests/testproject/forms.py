from django import forms
from .models import *


class SimpleModelForm(forms.ModelForm):
    class Meta:
        model = SimpleModel