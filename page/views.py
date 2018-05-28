# coding: utf-8
from __future__ import unicode_literals

from django.views.generic import TemplateView


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
