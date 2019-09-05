#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-5 上午9:08
# @Version        : 1.0
# @File           : serializers
# @Software       : PyCharm


from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer

from users.mixins import BulkSerializerMixin
from certs.models import Certs
from users.serializers import UserSerializer


class CertSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    证书的数据结构
    """

    class Meta:
        model = Certs
        list_serializer_class = BulkListSerializer
        fields = '__all__'
        validators = []

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.extend([
            'get_method'
        ])
        return fields
