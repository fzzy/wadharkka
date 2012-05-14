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
import difflib
import pickle
import json
import copy
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
    ctx = copy.copy(default_ctx)
    ctx['messages'] = messages
    return render_to_response('error.html', {'messages': messages}, RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('home')

@login_required
def done(request):
    """Login complete view, displays owned documents"""
    ctx = copy.copy(default_ctx)
    ctx['docs'] = Document.objects.filter(owner=request.user)
    return render_to_response('done.html', ctx, RequestContext(request))

@login_required
def shared_documents(request):
    """Display shared documents"""
    ctx = copy.copy(default_ctx)
    ctx['docs'] = request.user.document_contributors.all()
    return render_to_response('shared_documents.html', ctx, RequestContext(request))

@login_required
def profile(request):
    """Display user data"""
    ctx = copy.copy(default_ctx)
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
    ctx = copy.copy(default_ctx)
    ctx['form'] = form
    return render_to_response('create_document.html', ctx, RequestContext(request))

@login_required
def edit_document(request, id=None):
    """Edit a document"""
    ctx = copy.copy(default_ctx)
    if id is None:
        doc = None
        cur_revision = 0
    else:
        doc = get_object_or_404(Document, id=id)
        if request.user != doc.owner and not doc.contributors.filter(id=request.user.id).exists():
            raise Http404
        cur_revision = doc.revision
    if request.method == 'POST':
        # giving doc to the form may change its contents, so copy them now
        if doc is not None:
            cur_content = doc.content
        form = DocumentForm(request.POST, instance=doc)
        if form.is_valid():
            if cur_revision==form.cleaned_data['revision']:
                new_doc = form.save(commit=False)
                # update revision
                new_doc.revision = cur_revision + 1
                if doc is None:
                    # owner is not set when creating a new document
                    new_doc.owner = request.user
                new_doc.save()
                return redirect('show_document', new_doc.id)
            else:
                # document was changed during editing
                ctx['diff_warning'] = True
                ctx['cur_content'] = cur_content
                ctx['diff'] = ''.join(difflib.ndiff(doc.content.splitlines(1), cur_content.splitlines(1)))
    form = DocumentForm(instance=doc, initial={'revision': cur_revision })
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
    ctx = copy.copy(default_ctx)
    ctx['doc'] = doc
    return render_to_response('delete_document.html', ctx, RequestContext(request))

def show_document(request, id):
    """Show contents of a document"""
    ctx = copy.copy(default_ctx)
    doc = get_object_or_404(Document, id=id)
    if not (doc.visibility == 'A' or 
            (doc.visibility == 'R' and request.user.is_authenticated()) or
            (doc.visibility == 'C' and 
             (doc.owner==request.user or doc.contributors.filter(id=request.user.id).exists()))):
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
    ctx = copy.copy(default_ctx)
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
    """Return parsed markdown html code for markitup preview button"""
    if request.method == 'POST':
        data = request.POST.get('data', '')
        pdata = parse_md(data)
        return HttpResponse(pdata)
