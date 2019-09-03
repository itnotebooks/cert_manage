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
    url(r'^logout$', views.UserLogoutView.as_view(), name='logout'),

    # Profile
    url(r'^profile/$', views.UserProfileView.as_view(), name='user-profile'),
    url(r'^profile/update/$', views.UserProfileUpdateView.as_view(), name='user-profile-update'),
    url(r'^profile/password/update/$', views.UserPasswordUpdateView.as_view(), name='user-password-update'),

    # User view
    url(r'^user$', views.UserListView.as_view(), name='user-list'),
    url(r'^user/create$', views.UserCreateView.as_view(), name='user-create'),
    url(r'^user/(?P<pk>[0-9a-zA-Z\-]{36})/update$', views.UserUpdateView.as_view(), name='user-update'),
    url(r'^user/(?P<pk>[0-9a-zA-Z\-]{36})$', views.UserDetailView.as_view(), name='user-detail'),

    # User group view
    url(r'^user-group$', views.UserGroupListView.as_view(), name='user-group-list'),
    url(r'^user-group/(?P<pk>[0-9a-zA-Z\-]{36})$', views.UserGroupDetailView.as_view(), name='user-group-detail'),
    url(r'^user-group/create$', views.UserGroupCreateView.as_view(), name='user-group-create'),
    url(r'^user-group/(?P<pk>[0-9a-zA-Z\-]{36})/update$', views.UserGroupUpdateView.as_view(),
        name='user-group-update'),

]
