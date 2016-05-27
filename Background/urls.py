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
    url(r'^pilot/getMyTrend$',views.getOneTrend),
    url(r'^pilot/getMyCommentMessage$',views.getMyCommentMessage),
    url(r'^pilot/deleteCommentMessage$',views.deleteCommentMassage),
    url(r'^pilot/getMyXMoney$',views.getMyXMoney),
    url(r'^pilot/getUserGuanzhu$',views.getOnesUserFollow),
    url(r'^pilot/getUserFensi$',views.getOnesUserFollowers),
    url(r'^pilot/getUserDetail$',views.getUserDetail),
    url(r'^pilot/getTrendBriefMessage$',views.getTrendBriefMessage),
    url(r'^pilot/getBriefUser$',views.getBriefUser),

    # search
    url(r'^pilot/searchUser$',views.searchUser),

    # trend
    url(r'^trend/createTrend$',viewTrend.createTrend),
    url(r'^trend/getMyFollowTrends$',viewTrend.getMyFollowTrends),
    url(r'^trend/getTrendComment$',viewTrend.getTrendComment),
    url(r'^trend/commentTrend$',viewTrend.commentTrend),
    url(r'^trend/likeTrend$',viewTrend.likeTrend),
    url(r'^trend/getTrendById$',viewTrend.getTrendById),


]