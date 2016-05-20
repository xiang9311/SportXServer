__author__ = '祥祥'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^test/$', views.test),

    # token
    url(r'^token/getQiniuToken$', views.getQiniuToken),
    url(r'^token/getRongToken$', views.getRongToken),

    # pilot
    url(r'^pilot/verifyPhoneCanUse', views.verifyPhoneCanUse),
    url(r'^pilot/register$', views.register),
    url(r'^pilot/login$',views.login),

    # search
    url(r'^pilot/searchUser',views.searchUser),

]