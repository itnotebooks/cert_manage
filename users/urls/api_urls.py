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

urlpatterns = [
    url(r'^v1/logout/$', api.UserLogOut.as_view(), name='user-logout'),
    url(r'^v1/profile/$', api.UserProfile.as_view(), name='user-profile'),
    url(r'^v1/users/(?P<pk>[0-9a-zA-Z\-]{36})/password/$',
        api.ChangeUserPasswordApi.as_view(), name='change-user-password'),
    url(r'^v1/users/(?P<pk>[0-9a-zA-Z\-]{36})/groups/$',
        api.UserUpdateGroupApi.as_view(), name='user-update-group'),
    url(r'^v1/groups/(?P<pk>[0-9a-zA-Z\-]{36})/users/$',
        api.UserGroupUpdateUserApi.as_view(), name='user-group-update-user'),
    url(r'^v1/group-update/$', api.UserGroupCreateorUpdate.as_view(), name='user-group-update'),

]

urlpatterns += router.urls
