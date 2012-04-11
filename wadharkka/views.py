from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

default_dict = {}

def home(request):
    return render_to_response('home.html', default_dict, RequestContext(request))

