# coding: utf-8
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.generic import DetailView
from django.views.generic import ListView

from core.Mixin.StatusWrapMixin import StatusWrapMixin, ERROR_DATA
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin
from core.models import UniqueCode


class PhoneBindView(StatusWrapMixin, JsonResponseMixin, DetailView):
    model = UniqueCode
    include_attr = ['code']

    def get(self, request, *args, **kwargs):
        phone = request.GET.get('phone')
        token = request.GET.get('token')
        unique_code_list = UniqueCode.objects.filter(unique_id=token, use=False).all()
        phone_nums = UniqueCode.objects.filter(phone=phone).count()
        if unique_code_list.exists() and phone_nums < 2:
            unique_code = unique_code_list[0]
            unique_code.phone = phone
            unique_code.use = True
            if unique_code.code_type != 11:
                unique_code.save()
            # self.message = unique_code.code_type
            scode_type = {1: '10', 2: '30', 3: '50', 4: '60', 11: '50'}
            self.message = '成功领取{0}元电子券!'.format(scode_type.get(unique_code.code_type))
            return self.render_to_response({})
        self.message = '领券超出限制或无效'
        self.status_code = ERROR_DATA
        return self.render_to_response({})



