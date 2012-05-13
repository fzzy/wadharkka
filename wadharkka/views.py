# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
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
    ctx['docs'] = Document.objects.filter(owner=request.user)
    return render_to_response('done.html', ctx, RequestContext(request))

@login_required
def shared_documents(request):
    """Display shared documents"""
    ctx = default_ctx
    ctx['docs'] = request.user.document_contributors.all()
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
    if request.user != doc.owner and not doc.contributors.filter(id=request.user.id).exists():
        raise Http404
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=doc)
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
    if request.user != doc.owner:
        raise Http404
    if request.method == 'POST':
        doc.delete()
        return redirect('done')
    ctx = default_ctx
    ctx['doc'] = doc
    return render_to_response('delete_document.html', ctx, RequestContext(request))

def show_document(request, id):
    """Show contents of a document"""
    ctx = default_ctx
    doc = get_object_or_404(Document, id=id)
    if not \
            (doc.visibility == 'A' or \
            (doc.visibility == 'R' and request.user.is_authenticated()) or \
            (doc.visibility == 'C' and \
                 (doc.owner==request.user or doc.contributors.filter(id=request.user.id).exists())) or \
            (doc.visibility == 'O' and doc.owner.id==request.user.id)):
        raise Http404
    ctx['doc'] = doc
    ctx['doc'].content = parse_md(doc.content)
    return render_to_response('show_document.html', ctx, RequestContext(request))

@login_required
def share_document(request, id):
    """View for managing sharing of a document"""
    doc = get_object_or_404(Document, id=id)
    if request.user != doc.owner:
        raise Http404
    ctx = default_ctx
    ctx['success'] = False
    if request.method == 'POST':
        visibility_form = VisibilityForm(request.POST, instance=doc)
        emails = request.POST.getlist('conemails',[])
        if not isinstance(emails, list):
            emails = [emails]
        emails_pass = True
        emailsv = []
        # remove owner email, empty or errorneous emails
        for a in emails:
            if doc.owner.email==a or len(a) <= 0 or not validate_email(a):
                continue
            emailsv.append(a)
        if visibility_form.is_valid() and emails_pass:
            doc.visibility = visibility_form.cleaned_data['visibility']
            doc.contributors = User.objects.filter(email__in=emailsv)
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
