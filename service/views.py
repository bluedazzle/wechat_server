# coding: utf-8
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.generic import DetailView

from core.Mixin.StatusWrapMixin import StatusWrapMixin, ERROR_DATA
from core.dss.Mixin import JsonResponseMixin
from core.models import UniqueCode
from core.wechat_service import WeChatService


class MainServiceView(StatusWrapMixin, JsonResponseMixin, DetailView):
    model = UniqueCode
    include_attr = ['code']

    def get(self, request, *args, **kwargs):
        WS = WeChatService('wx586e2dfae97146a7', '226f8be53f435e54247470a39f907ec6')
        signature = request.GET.get('signature', '')  # Request 中 GET 参数 signature
        timestamp = request.GET.get('timestamp', '')  # Request 中 GET 参数 timestamp
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        if WS.wechat.check_signature(signature, timestamp, nonce):
            return HttpResponse(echostr)
        return HttpResponse(echostr)

    def post(self, request, *args, **kwargs):
        WS = WeChatService('wx586e2dfae97146a7', '226f8be53f435e54247470a39f907ec6')
        body_text = request.body
        response = WS.message_manage(body_text)
        return HttpResponse(response)
