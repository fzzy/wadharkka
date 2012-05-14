# -*- coding: utf-8 -*-
import models
from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase

class DocumentTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('urho', 'kaleva@kekkonen.com', 'urhopassu')
        self.doc1 = models.Document.objects.create(
            subject="foobar sub",
            content="foobar content",
            owner=self.user,
            visibility='R')
        self.doc2 = models.Document.objects.create(
            subject="twobar sub",
            content="twobar content",
            owner=self.user,
            visibility='A')

    def test_document_creation(self):
        self.assertEqual(self.doc1.id, 1)
        self.assertEqual(self.doc1.subject, 'foobar sub')
        self.assertEqual(self.doc1.content, 'foobar content')
        self.assertEqual(self.doc1.owner, self.user)
        self.assertEqual(self.doc1.visibility, 'R')

        self.assertEqual(self.doc2.id, 2)
        self.assertEqual(self.doc2.visibility, 'A')

    def test_show_document_permissions(self):
        response = self.c.get('/document/show/1/')
        self.assertEqual(response.status_code, 404)
        
        response = self.c.get('/document/show/2/')
        self.assertNotEqual(response.status_code, 404)

    def test_document_404_raise_permissions(self):
        response = self.c.get('/document/edit/1/')
        self.assertEqual(response.status_code, 302)
        response = self.c.post('/document/edit/1/')
        self.assertEqual(response.status_code, 302)

        response = self.c.get('/document/delete/1/')
        self.assertEqual(response.status_code, 302)
        response = self.c.post('/document/delete/1/')
        self.assertEqual(response.status_code, 302)

        response = self.c.get('/document/share/1/')
        self.assertEqual(response.status_code, 302)
        response = self.c.post('/document/share/1/')
        self.assertEqual(response.status_code, 302)

    def test_preview_parser(self):
        response = self.c.post('/preview_parser/', {'data': '`mycode`'})
        self.assertEqual(response.content, '<p><code>mycode</code></p>\n')



