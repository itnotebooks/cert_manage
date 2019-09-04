#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 下午4:25
# @Version        : 1.0
# @File           : authentication
# @Software       : PyCharm


import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework import authentication
from rest_framework.authtoken.models import Token

from .user import User


class AccessKey(models.Model):
    id = models.UUIDField(verbose_name='AccessKeyID', primary_key=True,
                          default=uuid.uuid4, editable=False)
    secret = models.UUIDField(verbose_name='AccessKeySecret',
                              default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, verbose_name='User',
                             on_delete=models.CASCADE, related_name='access_key')

    def get_id(self):
        return str(self.id)

    def get_secret(self):
        return str(self.secret)

    def __str__(self):
        return str(self.id)


class PrivateToken(Token):
    """Inherit from auth token, otherwise migration is boring"""

    class Meta:
        verbose_name = _('Private Token')
