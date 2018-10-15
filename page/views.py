# coding: utf-8
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import TemplateView

from core.models import UniqueCode, Shop


class PhonePageView(TemplateView):
    template_name = 'phone.html'

    def get_context_data(self, **kwargs):
        context = super(PhonePageView, self).get_context_data(**kwargs)
        token = self.request.GET.get('token', '')
        context['token'] = token
        context['title'] = '优惠券领取'
        return context


class HintPageView(TemplateView):
    template_name = 'hint.html'


class ShopListView(ListView):
    model = Shop
    template_name = 'shop.html'


class PhoneListView(ListView):
    template_name = 'hint.html'
    model = UniqueCode

    def get(self, request, *args, **kwargs):
        code_type = {1: '10元电子券', 2: '30元电子券', 3: '50元电子券', 4: '60元电子券'}
        queryset = self.get_queryset().filter(use=True).exclude(code_type__in=(10, 11)).order_by(
            '-modify_time')
        content = '时间 电话 优惠券<br>'
        for query in queryset:
            q_str = '{0} {1} {2}<br>'.format(query.modify_time.strftime('%Y-%m-%d %H:%M:%S'), query.phone, code_type.get(query.code_type, '未知'))
            content = '{0}{1}'.format(content, q_str)
        return HttpResponse(content)
