from django.shortcuts import render
from .service import trendService

# Create your views here.

def index(request):
    trends = trendService.getHotTrend()
    return render(request, 'SportXPark/index.html', {'trends':trends})