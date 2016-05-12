from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.

def test(request):
    return HttpResponse('ok')

def index(request):
    return HttpResponse('欢迎来到SportX')