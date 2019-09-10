#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 上午6:41
# @Version        : 1.0
# @File           : utils
# @Software       : PyCharm

from django.conf import settings

from django.utils.translation import ugettext as _
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache


def date_expired_default():
    try:
        years = int(settings.DEFAULT_EXPIRED_YEARS)
    except TypeError:
        years = 70
    return timezone.now() + timezone.timedelta(days=365 * years)


def get_tmp_user_from_cache(request):
    if not request.session.session_key:
        return None
    user = cache.get(request.session.session_key + 'user')
    return user


def set_tmp_user_to_cache(request, user):
    cache.set(request.session.session_key + 'user', user, 600)


def get_user_or_tmp_user(request):
    user = request.user
    tmp_user = get_tmp_user_from_cache(request)
    if user.is_authenticated:
        return user
    elif tmp_user:
        return tmp_user
    else:
        raise Http404("Not found this user")


def redirect_user_first_login_or_index(request, redirect_field_name):
    return request.POST.get(
        redirect_field_name,
        request.GET.get(redirect_field_name, reverse('index')))


def get_login_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')
    if x_forwarded_for and x_forwarded_for[0]:
        login_ip = x_forwarded_for[0]
    else:
        login_ip = request.META.get('REMOTE_ADDR', '')
    return login_ip


create_success_msg = _("<b>%(name)s</b> was created successfully")
update_success_msg = _("<b>%(name)s</b> was updated successfully")


def refresh_token(token, user, expiration=settings.TOKEN_EXPIRATION or 3600):
    cache.set(token, user.id, expiration)
