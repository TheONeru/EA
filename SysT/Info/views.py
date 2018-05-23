from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.

def account_info(request):
    return render(request, 'index.html')

def position_info(request):
    return HttpResponse("This page is position_info")
