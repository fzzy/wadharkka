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
from django.forms.models import modelformset_factory
from social_auth.utils import setting
from django.contrib.auth.models import User
from django.forms.models import formset_factory
from forms import DocumentForm, VisibilityForm
from models import Document
from datetime import datetime
from utils import parse_md, validate_email
import json
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
    """Login complete view, displays owned documents"""
    ctx = default_ctx
    ctx['owned_docs'] = Document.objects.filter(owner=request.user).values('id', 'subject', 'date')
    return render_to_response('done.html', ctx, RequestContext(request))

@login_required
def shared_documents(request):
    """Display shared documents"""
    ctx = default_ctx
    ctx['shared_docs'] = Document.objects.filter(owner=request.user).values('id', 'subject', 'date')
    return render_to_response('shared_documents.html', ctx, RequestContext(request))

@login_required
def profile(request):
    """Display user data"""
    ctx = default_ctx
    ctx['last_login'] = request.session.get('social_auth_last_login_backend')
    return render_to_response('profile.html', ctx, RequestContext(request))

@login_required
def create_document(request):
    """View for creating new documents"""
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            d = form.save(commit=False)
            d.owner = request.user
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
            form.save()
            return redirect('show_document', id)
    else:        
        form = DocumentForm(instance=doc)
    ctx = default_ctx
    ctx['doc'] = doc
    ctx['form'] = form
    return render_to_response('edit_document.html', ctx, RequestContext(request))

@login_required
def delete_document(request, id):
    """Delete a document"""
    doc = get_object_or_404(Document, id=id)
    if request.method == 'POST':
        doc.delete()
        return redirect('done')
    ctx = default_ctx
    ctx['doc'] = doc
    return render_to_response('delete_document.html', ctx, RequestContext(request))

def show_document(request, id):
    """Show contents of a document"""
    ctx = default_ctx
    ctx['doc'] = get_object_or_404(Document, id=id)
    ctx['doc'].content = parse_md(ctx['doc'].content)
    return render_to_response('show_document.html', ctx, RequestContext(request))

@login_required
def share_document(request, id):
    """View for managing sharing of a document"""
    doc = get_object_or_404(Document, id=id)
    ctx = default_ctx
    ctx['success'] = False
    if request.method == 'POST':
        visibility_form = VisibilityForm(request.POST, instance=doc)
        emails = request.POST.getlist('conemails',[])
        if not isinstance(emails, list):
            emails = [emails]
        emails_pass = True
        for a in emails:
            # skip empty fields
            if len(a) <= 0:
                continue
            if not validate_email(a):
                emails_pass = False
                # TODO: add proper error message for the user
                break
        if visibility_form.is_valid() and emails_pass:
            doc.visibility = visibility_form.cleaned_data['visibility']
            print "EE",emails
            doc.contributors = User.objects.filter(email__in=emails)
            doc.save()
            ctx['success'] = True
    else:
        visibility_form = VisibilityForm(instance=doc)
    conemails = list(doc.contributors.values_list("email", flat=True))
    # this shouldn't throw an exception
    ctx['conemails'] = json.dumps([{"conemails":x} for x in conemails])

    ctx['doc'] = doc
    ctx['visibility_form'] = visibility_form
    return render_to_response('share_document.html', ctx, RequestContext(request))

# TODO: fix csrf for this view
# ensure_csrf_cookie decorator does not work here for some reason...
@csrf_exempt
def preview_parser(request):
    if request.method == 'POST':
        data = request.POST.get('data', '')
        pdata = parse_md(data)
        return HttpResponse(pdata)
