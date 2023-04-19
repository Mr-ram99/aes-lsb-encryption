from django import forms
from .models import AudioModel, AudioModel2

class AudioForm(forms.ModelForm):
    """Form for the  encrypt image model"""
    class Meta:
        model = AudioModel
        fields = ('key', 'text', 'audio')
        widgets = {
            'key': forms.TextInput(attrs={'placeholder': 'Enter Key', 'class':'form-control'}),
            'text' : forms.Textarea(attrs={'placeholder': 'Enter Text', 'class':'form-control','cols': 20, 'rows': 8, 'style':'resize:none;'}),
            'audio': forms.FileInput(attrs={'placeholder': 'Upload Audio File', 'class':'form-control'}),
        }

class AudioForm2(forms.ModelForm):
    """Form for the decrypt  image model"""
    class Meta:
        model = AudioModel2
        fields = ('key','audio',)
        widgets = {
             'key': forms.TextInput(attrs={'placeholder': 'Enter Key', 'class':'form-control'}),
            'audio': forms.FileInput(attrs={'placeholder': 'Upload audio file', 'class':'form-control'}),
        }