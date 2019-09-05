#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-5 下午5:35
# @Version        : 1.0
# @File           : tasks
# @Software       : PyCharm
from celery import shared_task

from cert_manage.utils import certs_messages_remaind_email
from certs.models import Certs
from certs.utils import load_certificate


@shared_task
def refresh_certs_messages_to_db(cert_obj=None):
    '''
    此函数用于刷新证书的详细信息
    :return:
    '''
    if cert_obj:
        certs = Certs.objects.filter(id=cert_obj.id)
    else:
        certs = Certs.objects.all()

    for cert in certs:
        if not cert.method: cert.method = 0
        if cert.method == 0:
            cert_info = load_certificate(cert.method, cert.domain_url)
        else:
            cert_info = load_certificate(cert.method, cert.pem_file)

        for k, v in cert_info.items():
            setattr(cert, k, v)
            if k.startswith('remain_days'):
                if int(v) <= 90:
                    certs_messages_remaind_email(cert, cert_info)
        cert.save()
    return 0
