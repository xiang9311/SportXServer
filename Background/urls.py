__author__ = '祥祥'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^test/$', views.test),

    # token
    url(r'^token/getQiniuToken$', views.getQiniuToken),

    # pilot
    url(r'^pilot/register$', views.register),

]