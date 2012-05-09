# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import get_messages
from social_auth.utils import setting
import settings

default_ctx = {
    "APP_NAME": settings.APP_NAME,
    }

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('home.html', default_ctx, RequestContext(request))


@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = default_ctx
    ctx['last_login'] = request.session.get('social_auth_last_login_backend')

    return render_to_response('done.html', ctx, RequestContext(request))


def error(request):
    """Error view"""
    messages = get_messages(request)
    ctx = default_ctx
    ctx['messages'] = messages
    return render_to_response('error.html', {'messages': messages}, RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


def form(request):
    if request.method == 'POST' and request.POST.get('username'):
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        request.session['saved_username'] = request.POST['username']
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('form.html', default_ctx, RequestContext(request))

def editor(request):
    return render_to_response('editor.html', default_ctx, RequestContext(request))

