#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 上午7:19
# @Version        : 1.0
# @File           : views_urls
# @Software       : PyCharm


from django.conf.urls import url
from certs import views

app_name = 'certs'

urlpatterns = [
    # 证书
    url(r'^$', views.CertListView.as_view(), name='cert-index'),
    url(r'^create/$', views.CertCreateView.as_view(), name='cert-create'),
    url(r'^(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.CertUpdateView.as_view(),
        name='cert-update'),
    url(r'^(?P<pk>[0-9a-zA-Z\-]{36})/$', views.CertDetailView.as_view(), name='cert-detail'),
]
