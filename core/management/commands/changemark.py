# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from core.models import UniqueCode
from core.utils import create_unique
from core.wechat_service import WeChatService


class Command(BaseCommand):
    def handle(self, *args, **options):
        for uc in UniqueCode.objects.all():
            uc.use = False
            uc.phone = ''
            uc.save()
        # ws = WeChatService('wx586e2dfae97146a7', '226f8be53f435e54247470a39f907ec6')
        # # nums = {'10': 2, '30': 150, '50': 20, '60': 20}
        # nums = {'10': 2}
        # code_type = {'10': 1, '30': 2, '50': 3, '60': 4}
        # for k, v in nums.items():
        #     print '{0} yuandianziquan'.format(k)
        #     for i in xrange(v):
        #         token = '{0}{1}'.format(create_unique(8), k)
        # # token = create_unique(10)
        #         ticket, url = ws.create_qrcode(token)
        #         print '{0}'.format(url)
        #         uc = UniqueCode(unique_id=token, code_type=code_type.get(k), qr_content=url, qr_url=ticket)
        #         uc.save()

