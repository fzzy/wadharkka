# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import get_messages
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from social_auth.utils import setting
from forms import DocumentForm
from models import Document
from datetime import datetime
from utils import parse_md
import settings

default_ctx = {
    "APP_NAME": settings.APP_NAME,
    }

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')
    else:
        return render_to_response('home.html', default_ctx, RequestContext(request))

def error(request):
    """Error view"""
    messages = get_messages(request)
    ctx = default_ctx
    ctx['messages'] = messages
    return render_to_response('error.html', {'messages': messages}, RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('home')

@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = default_ctx
    ctx['last_login'] = request.session.get('social_auth_last_login_backend')
    ctx['owned_docs'] = Document.objects.filter(owner=request.user).values('id', 'subject', 'date')
    return render_to_response('done.html', ctx, RequestContext(request))

@login_required
def create_document(request):
    """View for creating new documents"""
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            d = Document(subject=subject, content=content, owner=request.user)
            d.save()
            return redirect('show_document', d.id)
    else:
        form = DocumentForm()
    ctx = default_ctx
    ctx['form'] = form
    return render_to_response('create_document.html', ctx, RequestContext(request))

@login_required
def edit_document(request, id):
    """Edit an existing document"""
    doc = get_object_or_404(Document, id=id)
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            doc.subject = form.cleaned_data['subject']
            doc.content = form.cleaned_data['content']
            doc.save()
            return redirect('show_document', id)
    else:        
        form = DocumentForm(instance=doc)
    ctx = default_ctx
    ctx['doc'] = doc
    ctx['form'] = form
    return render_to_response('edit_document.html', ctx, RequestContext(request))

def show_document(request, id):
    """Show contents of a document"""
    ctx = default_ctx
    ctx['doc'] = get_object_or_404(Document, id=id)
    ctx['doc'].content = parse_md(ctx['doc'].content)
    return render_to_response('show_document.html', ctx, RequestContext(request))

@csrf_exempt
def preview_parser(request):
    if request.method == 'POST':
        data = request.POST.get('data', '')
        pdata = parse_md(data)
        return HttpResponse(pdata)
