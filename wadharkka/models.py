# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

class Document(models.Model):
    name = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    date = models.DateTimeField('date posted', editable=False, default=datetime.now)
    
    def __unicode__(self):
        return self.name

    class Admin:
        pass

class Diff(models.Model):
    document = models.ForeignKey(Document)
    diff = models.TextField()
    date = models.DateTimeField('date posted', editable=False)
    
    def __unicode__(self):
        return self.keyword

    class Admin:
        pass
