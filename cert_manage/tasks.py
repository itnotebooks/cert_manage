#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-5 下午5:26
# @Version        : 1.0
# @File           : tasks
# @Software       : PyCharm
from .celery import app
from django.core.mail import send_mail
from django.conf import settings


@app.task
def send_mail_async(*args, **kwargs):
    """ Using celery to send email async

    You can use it as django send_mail function

    Example:
    send_mail_sync.delay(subject, message, from_mail, recipient_list, fail_silently=False, html_message=None)

    Also you can ignore the from_mail, unlike django send_mail, from_email is not a require args:

    Example:
    send_mail_sync.delay(subject, message, recipient_list, fail_silently=False, html_message=None)
    """
    if len(args) == 3:
        args = list(args)
        args[0] = settings.EMAIL_SUBJECT_PREFIX + args[0]
        args.insert(2, settings.EMAIL_HOST_USER)
        args = tuple(args)

    try:
        send_mail(*args, **kwargs)
    except Exception as e:
        print("Sending mail error: {}".format(e))
