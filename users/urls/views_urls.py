#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 上午7:15
# @Version        : 1.0
# @File           : views_urls
# @Software       : PyCharm

from __future__ import absolute_import

from django.conf.urls import url

from users import views

app_name = 'users'

urlpatterns = [
    # Login view
    url(r'^login$', views.UserLoginView.as_view(), name='login'),
    url(r'^logout$', views.UserLogoutView.as_view(), name='logout')
]
