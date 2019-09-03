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


class UserSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    groups_display = serializers.SerializerMethodField()
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=UserGroup.objects.all(), required=False)

    class Meta:
        model = User
        list_serializer_class = BulkListSerializer
        fields = ['id', 'name', 'username', 'role', 'phone', 'groups', 'is_active', 'email', 'date_expired']

    def get_field_names(self, declared_fields, info):
        fields = super(UserSerializer, self).get_field_names(declared_fields, info)
        fields.extend([
            'groups_display', 'is_valid'
        ])

        return fields

    @staticmethod
    def get_groups_display(obj):
        return " ".join([group.name for group in obj.groups.all()])


class UserGroupSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = UserGroup
        list_serializer_class = BulkListSerializer
        fields = '__all__'

    @staticmethod
    def get_users(obj):
        user_list = []
        for user in obj.users.all():
            user_list.append({'id': user.id, 'name': user.name})
        return user_list


class ChangeUserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class UserUpdateGroupSerializer(serializers.ModelSerializer):
    groups = UserGroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'groups']

    def get_field_names(self, declared_fields, info):
        fields = super(UserUpdateGroupSerializer, self).get_field_names(declared_fields, info)
        fields.extend([
            'unselect_groups'
        ])

        return fields


class UserGroupUpdateOrCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'groups']


class UserGroupUpdateMemeberSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = UserGroup
        fields = ['id', 'users']