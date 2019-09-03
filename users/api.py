#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 上午7:16
# @Version        : 1.0
# @File           : api
# @Software       : PyCharm

from django.contrib.auth import logout

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_bulk import BulkModelViewSet

from users.serializers import UserSerializer, UserGroupSerializer, UserUpdateGroupSerializer, \
    ChangeUserPasswordSerializer, UserGroupUpdateOrCreateSerializer, UserGroupUpdateMemeberSerializer

from users.models import User, UserGroup
from users.permissions import IsSuperUser, IsValidUser
from users.mixins import IDInFilterMixin


class UserViewSet(IDInFilterMixin, BulkModelViewSet):
    '''
    用户的操作接口
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsSuperUser,)
    filter_fields = ('username', 'email', 'name', 'phone', 'date_expired')
    search_fields = filter_fields


class UserGroupViewSet(IDInFilterMixin, BulkModelViewSet):
    '''
    用户组的操作接口
    '''
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsSuperUser,)
    search_fields = ('name', 'comment')


class UserLogOut(APIView):
    '''
    注销登录
    '''
    permission_classes = (AllowAny,)

    def post(self, request):
        logout(request)
        return Response({})


class UserProfile(APIView):
    '''
    用户信息
    '''
    permission_classes = (IsValidUser,)
    serializer_class = UserSerializer

    def get(self, request):
        # return Response(request.user.to_json())
        return Response(self.serializer_class(request.user).data)

    def post(self, request):
        return Response(self.serializer_class(request.user).data)


class ChangeUserPasswordApi(generics.RetrieveUpdateAPIView):
    '''
    用户修改密码接口
    '''
    permission_classes = (IsSuperUser,)
    queryset = User.objects.all()
    serializer_class = ChangeUserPasswordSerializer

    def perform_update(self, serializer):
        user = self.get_object()
        user.password_raw = serializer.validated_data["password"]
        user.save()


class UserUpdateGroupApi(generics.RetrieveUpdateAPIView):
    '''
    组更新接口
    '''
    queryset = User.objects.all()
    serializer_class = UserUpdateGroupSerializer
    permission_classes = (IsSuperUser,)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return UserGroupUpdateOrCreateSerializer
        return self.serializer_class


class UserGroupUpdateUserApi(generics.RetrieveUpdateAPIView):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupUpdateMemeberSerializer
    permission_classes = (IsSuperUser,)


class UserGroupCreateorUpdate(IDInFilterMixin, APIView):
    permission_classes = (IsSuperUser,)
    http_method_names = ['post']

    def post(self, request, **kwargs):
        try:
            name = request.data.get("name")
            comment = request.data.get("comment")
            users = request.data.get("users")

            defaults = {
                'name': name,
                'comment': comment
            }
            usergroup = UserGroup.objects.update_or_create(
                defaults=defaults, name=name
            )
            usergroup[0].users.set(users)
        except Exception as ex:
            return Response({"result": "Error: {}".format(ex)}, status=201)
        return Response({"result": "Success"}, status=200)
