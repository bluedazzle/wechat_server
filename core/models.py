# coding: utf-8
from __future__ import unicode_literals
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UniqueCode(BaseModel):
    code_choices = (
        (1, '10元电子券'),
        (2, '30元电子券'),
        (3, '50元电子券'),
        (4, '60元电子券'),
        (10, '导航'),
        (11, '测试'),

    )
    unique_id = models.CharField(max_length=64, unique=True)
    code_type = models.IntegerField(default=1, choices=code_choices)
    qr_content = models.CharField(max_length=256, default='', null=True, blank=True)
    qr_url = models.CharField(max_length=256, default='', null=True, blank=True)
    phone = models.CharField(max_length=20, default='', null=True, blank=True)
    use = models.BooleanField(default=False)

    def __unicode__(self):
        return '{0}-{1}-{2}-{3}'.format(self.unique_id, self.qr_content,  self.use, self.phone)


class WeChatAdmin(models.Model):
    name = models.CharField(max_length=128, default='', null=True, blank=True)
    app_id = models.CharField(max_length=128, default='', null=True, blank=True)
    app_secret = models.CharField(max_length=128, default='', null=True, blank=True)
    access_token = models.CharField(max_length=1024, default='', null=True, blank=True)

    def __unicode__(self):
        return self.app_id
