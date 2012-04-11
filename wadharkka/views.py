from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

default_dict = {}

def editor(request):
    return render_to_response('editor.html', default_dict, RequestContext(request))

