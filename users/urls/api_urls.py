#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 上午7:14
# @Version        : 1.0
# @File           : api_urls
# @Software       : PyCharm


from __future__ import absolute_import

from django.conf.urls import url
from rest_framework_bulk.routes import BulkRouter
from users import api

app_name = 'users'

router = BulkRouter()
router.register(r'v1/users', api.UserViewSet, 'user')
router.register(r'v1/groups', api.UserGroupViewSet, 'user-group')

urlpatterns = []

urlpatterns += router.urls
