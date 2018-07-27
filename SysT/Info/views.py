from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from . import views_code, ec_func
import json
import re

def index(request):
    r=views_code.get_info(request)
    x=render(request, 'Info/index.html', r)
    return render(request, 'Info/index.html', r)

def reload_info(request):
    r=views_code.get_info(request)
    x=json.dumps(r)
    return HttpResponse(x)

def change_state(request):
    views_code.manage_trade(request)
    return HttpResponseRedirect("../")
    

