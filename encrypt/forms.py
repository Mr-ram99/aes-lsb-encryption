from django import forms
from .models import ImageModel, ImageModel2

class ImageForm(forms.ModelForm):
    """Form for the  encrypt image model"""
    class Meta:
        model = ImageModel
        fields = ('key', 'text', 'image')
        widgets = {
            'key': forms.TextInput(attrs={'placeholder': 'Enter Key', 'class':'form-control'}),
            'text' : forms.Textarea(attrs={'placeholder': 'Enter Text', 'class':'form-control','cols': 20, 'rows': 8, 'style':'resize:none;'}),
            'image': forms.FileInput(attrs={'placeholder': 'Upload Image', 'class':'form-control'}),
        }

class ImageForm2(forms.ModelForm):
    """Form for the decrypt  image model"""
    class Meta:
        model = ImageModel2
        fields = ('key', 'image')
        widgets = {
            'key': forms.TextInput(attrs={'placeholder': 'Enter Key', 'class':'form-control'}),
            'image': forms.FileInput(attrs={'placeholder': 'Upload Image', 'class':'form-control'}),
        }