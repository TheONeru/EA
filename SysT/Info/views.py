from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from . import views_code
import json

# Create your views here.

def index(request):
    r=views_code.get_info(request)
    if(type(r)==dict):
        return render(request, 'Info/index.html', r)
    else:
        return HttpResponse(r)

def position_info(request):
    return HttpResponse("This page is position_info")

def reload_info(request):
    r=views_code.get_info(request)
    x=json.dumps(r)
    return HttpResponse(x)

def change_state(request):
    views_code.manage_trade(request)
    return HttpResponseRedirect("../")

    
