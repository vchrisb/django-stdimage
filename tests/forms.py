from django import forms

from .models import (SimpleModel, ResizeCropModel, MaxSizeModel)


class SimpleModelForm(forms.ModelForm):
    class Meta:
        model = SimpleModel


class ResizeCropModelForm(forms.ModelForm):
    class Meta:
        model = ResizeCropModel


class MaxSizeModelForm(forms.ModelForm):
    class Meta:
        model = MaxSizeModel