__author__ = '祥祥'
from django.conf.urls import url
from . import views, viewTrend, viewGym

urlpatterns = [
    # url(r'^createGym/$', views.createGyms),
    url(r'^test/$', views.test),

    # token
    url(r'^token/getQiniuToken$', views.getQiniuToken),
    url(r'^token/getRongyunToken$', views.getRongToken),

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
    url(r'^pilot/getRecommendUser$' , views.getRecommendUser),

    # search
    url(r'^pilot/searchUser$',views.searchUser),
    url(r'^pilot/searchGym$',views.searchGym),
    url(r'^pilot/getSearchKeys' , views.getSearchKeys),

    # trend
    url(r'^trend/createTrend$',viewTrend.createTrend),
    url(r'^trend/getMyFollowTrends$',viewTrend.getMyFollowTrends),
    url(r'^trend/getTrendComment$',viewTrend.getTrendComment),
    url(r'^trend/commentTrend$',viewTrend.commentTrend),
    url(r'^trend/likeTrend$',viewTrend.likeTrend),
    url(r'^trend/getTrendById$',viewTrend.getTrendById),


    #gym
    url(r'^gym/getGymList$',viewGym.getGymList),
    url(r'^gym/getGymDetail$',viewGym.getGymDetail),
    url(r'^gym/getRecommendGym$',viewGym.getRecommendGym),
    url(r'^gym/getGymTrend$',viewGym.getGymTrend),



]