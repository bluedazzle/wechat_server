# coding: utf-8
from __future__ import unicode_literals
import json
import requests
import simplejson
import redis

from core.models import WeChatAdmin, UniqueCode
from wechat_sdk import WechatBasic


class WeChatService(object):
    def __init__(self, app_id=None, app_secret=None):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=1)
        self.app_id = app_id
        self.app_secret = app_secret
        if not app_id:
            self.wechat_admin = WeChatAdmin.objects.all().order_by('id')[1]
            self.wechat = WechatBasic(appid=self.wechat_admin.app_id,
                                      appsecret=self.wechat_admin.app_secret,
                                      token=self.wechat_admin.access_token)
            self.app_id = self.wechat_admin.app_id
            self.app_secret = self.wechat_admin.app_secret
        else:
            self.wechat_admin = None
            self.wechat = WechatBasic(appid=app_id, appsecret=app_secret, token='123')

        self.get_token()

    def get_token(self):
        key = 'access_token_{0}'.format(self.app_id)
        token = self.redis.get(key)
        if not token:
            res = self.wechat.grant_token()
            token = res.get('access_token')
            self.redis.set(key, token, 3500)
            if self.wechat_admin:
                self.wechat_admin.access_token = token
                self.wechat_admin.save()
        return token

    def send_message(self, open_id, message):
        token = self.get_token()
        req_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}'.format(token)
        message = message.decode('utf-8')
        data = {'touser': open_id,
                'msgtype': 'text',
                'text': {'content': str('测试')}}
        result = requests.post(req_url, data=simplejson.dumps(data))
        return json.loads(result.content)

    def get_kefu_list(self):
        token = self.get_token()
        req_url = 'https://api.weixin.qq.com/cgi-bin/customservice/getkflist?access_token={0}'.format(token)
        result = requests.get(req_url)
        return json.loads(result.content)

    def distribution_kefu(self, open_id, account, extra_mes):
        token = self.get_token()
        req_url = 'https://api.weixin.qq.com/customservice/kfsession/create?access_token={0}'.format(token)
        data = {'kf_account': account,
                'openid': open_id,
                'text': extra_mes}
        result = requests.post(req_url, data=json.dumps(data))
        return result

    def create_qrcode(self, scene):
        data = {"action_name": "QR_LIMIT_STR_SCENE", "action_info": {"scene": {"scene_str": scene}}}
        result = self.wechat.create_qrcode(data)
        ticket = result.get('ticket', '')
        url = result.get('url', '')
        return ticket, url

    def get_user_info_by_code(self, code):
        req_url = '''https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'''.format(
            self.wechat_admin.app_id, self.wechat_admin.app_secret, code)
        result = requests.get(req_url)
        return json.loads(result.content)

    def get_promotion_info(self, openID, channel=None):
        result = Promotion.objects.filter(open_id=openID)
        if result.exists():
            return result[0]
        user_info = self.wechat.get_user_info(openID)
        nick = user_info.get('nickname', None)
        city = user_info.get('city', None)
        province = user_info.get('province', None)
        sex = '男'
        if str(user_info.get('sex', 0)) == '2':
            sex = '女'
        elif str(user_info.get('sex', 0)) == '0':
            sex = '未知'
        new_promotion = Promotion(open_id=openID,
                                  nick=nick,
                                  sex=sex,
                                  city=city,
                                  province=province,
                                  channel=channel)
        new_promotion.save()
        return new_promotion

    def message_manage(self, message_body):
        self.wechat.parse_data(message_body)
        message = self.wechat.get_message()
        manage_dict = {'text': self.text_manage,
                       'image': self.other_manage,
                       'video': self.other_manage,
                       'shortvideo': self.other_manage,
                       'link': self.other_manage,
                       'location': self.other_manage,
                       'subscribe': self.event_manage,
                       'unsubscribe': self.event_manage,
                       'scan': self.event_manage,
                       'view': self.event_manage,
                       'event': self.event_manage,
                       'voice': self.other_manage,
                       'click': self.click_manage
                       }
        result = manage_dict[message.type](message)
        response = self.wechat.response_text(result)
        return response

    def other_manage(self, message):
        pass

    def click_manage(self, message):
        pass

    def text_manage(self, message):
        return 'test'

    def event_manage(self, message):
        if message.type == 'subscribe':
            return self.handle_coupon(message)
        elif message.type == 'scan':
            return self.handle_coupon(message)

    def handle_coupon(self, message):
        key = message.key
        if key.startswith('qrscene_'):
            unique_id = key.split('qrscene_')[1]
        else:
            unique_id = key
        uc = UniqueCode.objects.filter(unique_id=unique_id).all()
        if uc.exists():
            uc = uc[0]
            if uc.code_type == 10:
                return "<a href='https://map.baidu.com/mobile/webapp/index/index#search/search/qt=s&wd=%E8%BF%9C%E5%A4%A7%E6%B1%BD%E4%BF%AE&c=328&searchFlag=bigBox&version=5&exptype=dep&src_from=webapp_all_bigbox&wd2=%E8%BF%90%E5%9F%8E%E5%B8%82%E7%9B%90%E6%B9%96%E5%8C%BA&sug_forward=a12baa40879e0355e956fa89&src=1/vt=map'>导航</a>"
            if uc.code_type == 11:
                return 'http://sy.chafanbao.com/page/phone/?token={0}'.format(unique_id)
            if not uc.use:
                return 'http://sy.chafanbao.com/page/phone/?token={0}'.format(unique_id)
        return '优惠券已被领取'
