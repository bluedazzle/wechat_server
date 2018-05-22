# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from core.models import UniqueCode
from core.utils import create_unique
from core.wechat_service import WeChatService


class Command(BaseCommand):
    def handle(self, *args, **options):
        ws = WeChatService('wx586e2dfae97146a7', '226f8be53f435e54247470a39f907ec6')
        nums = {'10': 50, '30': 150, '50': 20, '60': 20}
        code_type = {'10': 1, '30': 2, '50': 3, '60': 4}
        # for k, v in nums.items():
        #     for i in xrange(v):
        k = '10'
        token = '{0}{1}'.format(create_unique(8), k)
        ticket, url = ws.create_qrcode(token)
        print '{0}\r\n'.format(url)
        uc = UniqueCode(unique_id=token, code_type=code_type.get(k), qr_content=url, qr_url=ticket)
        uc.save()
