from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .dependency import pilot_pb2
from .service import  toaddService as userService
from .views import initCommonErrorResponse, initCommonResponse
from SportXServer import qiniuUtil, timeUtil ,log


