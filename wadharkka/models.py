# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Document(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    owner = models.ForeignKey(User, related_name='document_owner')
    contributors = models.ManyToManyField(User, blank=True, related_name='document_contributors')
    date = models.DateTimeField('date posted', editable=False, auto_now=True)
    revision = models.IntegerField(default=0, editable=False)

    VISIBILITY_CHOICES = (
        ('A', 'All'),
        ('R', 'Registered only'),
        ('C', 'Owner and contributors only'),
    )
    visibility = models.CharField(max_length=1, choices=VISIBILITY_CHOICES, default='A')
    
    def __unicode__(self):
        return self.subject
