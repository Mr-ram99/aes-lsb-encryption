from django import forms
from .models import ImageModel, ImageModel2

class ImageForm(forms.ModelForm):
    """Form for the  encrypt image model"""
    class Meta:
        model = ImageModel
        fields = ('title', 'text', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter Title', 'class':'form-control'}),
            'text' : forms.Textarea(attrs={'placeholder': 'Enter Text', 'class':'form-control','cols': 20, 'rows': 8, 'style':'resize:none;'}),
            'image': forms.FileInput(attrs={'placeholder': 'Upload Image', 'class':'form-control'}),
        }

class ImageForm2(forms.ModelForm):
    """Form for the decrypt  image model"""
    class Meta:
        model = ImageModel2
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(attrs={'placeholder': 'Upload Image', 'class':'form-control'}),
        }