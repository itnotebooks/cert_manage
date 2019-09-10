#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 上午7:19
# @Version        : 1.0
# @File           : api_urls
# @Software       : PyCharm

from certs import api

from rest_framework_bulk.routes import BulkRouter

app_name = 'certs'

router = BulkRouter()

# 证书
router.register(r'v1/cert', api.CertViewSet, 'cert')

urlpatterns = []
urlpatterns += router.urls
