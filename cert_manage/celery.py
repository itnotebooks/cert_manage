#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-4 上午7:01
# @Version        : 1.0
# @File           : celery
# @Software       : PyCharm

import os

from celery import Celery
from django.conf import settings

C_FORCE_ROOT = True

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cert_manage.settings')

app = Celery('cert_manage', backend=settings.CELERY_BROKER_URL, broker=settings.CELERY_BROKER_URL)

app.conf.timezone = 'Asia/Shanghai'

app.conf.update(
    task_serializer='json',
    accept_content=['json', 'pickle'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
)

FORKS = 60
TIMEOUT = 180
PERIOD_TASK = os.environ.get("PERIOD_TASK", "on")
