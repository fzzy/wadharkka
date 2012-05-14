# -*- coding: utf-8 -*-
from django import forms
from models import Document

class DocumentForm(forms.ModelForm):
    """Form for editing a document"""
    revision = forms.IntegerField(widget=forms.HiddenInput())
    
    class Meta:
        model = Document
        fields = ('subject', 'content')
        widgets = {
            'subject': forms.TextInput(attrs={'class':'span4'}),
            'content': forms.Textarea(),
            }

class VisibilityForm(forms.ModelForm):
    """Form for managing visibility option of a document"""
    class Meta:
        model = Document
        fields = ('visibility',)


