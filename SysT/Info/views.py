from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from . import views_code
import json
import time

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
    start=time.time()
    r=views_code.get_info(request)
    print("Reload1",time.time()-start)
    x=json.dumps(r)
    print("Reload2",time.time()-start)
    return HttpResponse(x)

def change_state(request):
    views_code.manage_trade(request)
    return HttpResponseRedirect("../")

    
