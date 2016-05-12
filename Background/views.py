from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.

def test(request):
    return HttpResponse('ok')