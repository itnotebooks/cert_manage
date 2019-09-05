#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 下午4:29
# @Version        : 1.0
# @File           : utils
# @Software       : PyCharm
import time
import base64
import calendar
import hashlib
import threading

from datetime import datetime
from email.utils import formatdate

from django.utils.translation import ugettext as _
from django.contrib.auth.mixins import UserPassesTestMixin

from cert_manage.tasks import send_mail_async


class AdminUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        elif not self.request.user.is_superuser:
            self.raise_exception = True
            return False
        return True


def content_md5(data):
    """计算data的MD5值，经过Base64编码并返回str类型。

    返回值可以直接作为HTTP Content-Type头部的值
    """
    if isinstance(data, str):
        data = hashlib.md5(data.encode('utf-8'))
    value = base64.b64encode(data.hexdigest().encode('utf-8'))
    return value.decode('utf-8')


_STRPTIME_LOCK = threading.Lock()

_GMT_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
_ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"


def to_unixtime(time_string, format_string):
    time_string = time_string.decode("ascii")
    with _STRPTIME_LOCK:
        return int(calendar.timegm(time.strptime(time_string, format_string)))


def http_date(timeval=None):
    """返回符合HTTP标准的GMT时间字符串，用strftime的格式表示就是"%a, %d %b %Y %H:%M:%S GMT"。
    但不能使用strftime，因为strftime的结果是和locale相关的。
    """
    return formatdate(timeval, usegmt=True)


def http_to_unixtime(time_string):
    """把HTTP Date格式的字符串转换为UNIX时间（自1970年1月1日UTC零点的秒数）。

    HTTP Date形如 `Sat, 05 Dec 2015 11:10:29 GMT` 。
    """
    return to_unixtime(time_string, _GMT_FORMAT)


def iso8601_to_unixtime(time_string):
    """把ISO8601时间字符串（形如，2012-02-24T06:07:48.000Z）转换为UNIX时间，精确到秒。"""
    return to_unixtime(time_string, _ISO8601_FORMAT)


def make_signature(access_key_secret, date=None):
    if isinstance(date, bytes):
        date = bytes.decode(date)
    if isinstance(date, int):
        date_gmt = http_date(date)
    elif date is None:
        date_gmt = http_date(int(time.time()))
    else:
        date_gmt = date

    data = str(access_key_secret) + "\n" + date_gmt
    return content_md5(data)


def encrypt_password(password, salt=None):
    from passlib.hash import sha512_crypt
    if password:
        return sha512_crypt.using(rounds=5000).hash(password, salt=salt)
    return None


def get_object_or_none(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    return obj


def certs_messages_remaind_email(cert, cert_info):
    base_message = '还有Days天到期'
    if int(cert_info.get('remain_days')) == 0:
        message = '已到期'
    elif int(cert_info.get('remain_days')) < 0:
        message = '已过期'
    elif int(cert_info.get('remain_days')) in [90, 60, 45, 30, 15] or int(cert_info.get('remain_days')) <= 14:
        message = base_message.replace('Days', str(cert_info.get('remain_days')))
    else:
        message = None

    if message:
        if len(cert_info.get('orther_domain')) > 0:
            orther_domain = [domain[1] for domain in cert_info.get('orther_domain')]
        else:
            orther_domain = cert_info.get('orther_domain')
        subject = _('重要通知：%(domain)s证书到期提醒(%(time)s)') % {'domain': cert_info.get('domain'),
                                                          'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        recipient_list = [user.email for user in cert.users.all()]
        message = _("""
        艾瑞巴蒂~</br>
        </br>
        %(domain)s证书%(message)s，避免影响业务的正常运行请及时更新。</br>
        =========================================================</br>
        颁发机构: %(issued_by)s</br>
        证书类型: %(cert_type)s</br>
        域名信息: %(domain)s</br>
        备用域名: %(orther_domain)s</br>
        有效期至: %(notafter)s</br>
        =========================================================</br>
        """) % {
            'domain': cert_info.get('domain'),
            'message': message,
            'issued_by': cert_info.get('issued_by'),
            'cert_type': cert_info.get('cert_type'),
            'orther_domain': orther_domain,
            'notafter': cert_info.get('notafter'),
        }

        send_mail_async.delay(subject, message, recipient_list, html_message=message)
