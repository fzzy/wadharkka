# -*- coding: utf-8 -*-
from django.forms import ModelForm, TextInput, Textarea
from models import Document 

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('subject', 'content')
        widgets = {
            'subject': TextInput(attrs={'class':'span4'}),
            'content': Textarea(),
            }

class SharingForm(ModelForm):
    class Meta:
        model = Document
        fields = ('visibility',)

