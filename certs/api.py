#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 上午7:22
# @Version        : 1.0
# @File           : api
# @Software       : PyCharm


from users.mixins import IDInFilterMixin
from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from users.permissions import IsSuperUser
from certs import serializers
from certs.models import Certs


class CertViewSet(IDInFilterMixin, BulkModelViewSet):
    """
    证书操作接口
    """
    filter_fields = ('name', 'domain', 'orther_domain', 'organization_name', 'cert_type', 'comment')
    search_fields = filter_fields
    ordering_fields = ('domain',)
    queryset = Certs.objects.all()
    serializer_class = serializers.CertSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsSuperUser,)
