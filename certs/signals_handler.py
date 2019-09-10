#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-5 下午5:37
# @Version        : 1.0
# @File           : signals_handler
# @Software       : PyCharm

from django.db.models.signals import post_save
from django.dispatch import receiver

from certs.tasks import refresh_certs_messages_to_db

from certs.models import Certs


@receiver(post_save, sender=Certs)
def certs_pre_create_or_update(sender, instance, **kwargs):
    refresh_certs_messages_to_db.delay(instance.id)
    return instance
