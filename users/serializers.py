#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 上午9:37
# @Version        : 1.0
# @File           : serializers
# @Software       : PyCharm


from rest_framework import serializers

from rest_framework_bulk import BulkListSerializer
from users.mixins import BulkSerializerMixin
from users.models import User, UserGroup


class UserGroupSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class UserSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    groups = UserGroupSerializer(many=True)

    class Meta:
        model = User
        list_serializer_class = BulkListSerializer
        fields = ['id', 'name', 'username', 'first_name', 'last_name', 'role', 'phone', 'groups', 'is_active', 'email',
                  'date_expired']
