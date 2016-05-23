__author__ = '祥祥'
from django.conf.urls import url
from . import views, viewTrend

urlpatterns = [
    url(r'^test/$', views.test),

    # token
    url(r'^token/getQiniuToken$', views.getQiniuToken),
    url(r'^token/getRongToken$', views.getRongToken),

    # pilot
    url(r'^pilot/verifyPhoneCanUse$', views.verifyPhoneCanUse),
    url(r'^pilot/register$', views.register),
    url(r'^pilot/updateMyInfo$', views.updateMyInfo),
    url(r'^pilot/login$',views.login),
    url(r'^pilot/guanzhuUser$',views.guanzhuUser),

    # search
    url(r'^pilot/searchUser$',views.searchUser),

    # trend
    url(r'^trend/createTrend$',viewTrend.createTrend),

]