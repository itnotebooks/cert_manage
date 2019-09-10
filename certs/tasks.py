#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-5 下午5:35
# @Version        : 1.0
# @File           : tasks
# @Software       : PyCharm
from cert_manage.celery import app

from cert_manage.utils import certs_messages_remaind_email
from certs.models import Certs
from certs.utils import load_certificate


@app.task
def refresh_certs_messages_to_db(cert_obj_id=None):
    '''
    此函数用于刷新证书的详细信息
    :return:
    '''
    certs = Certs.objects.filter(id=cert_obj_id) if cert_obj_id else Certs.objects.all()

    for cert in certs:

        Certs._meta.auto_created = True
        try:
            if not cert.method: cert.method = 0
            if cert.method == 0:
                cert_info = load_certificate(cert.method, cert.domain_url)
            else:
                cert_info = load_certificate(cert.method, cert.crt_file)

            for k, v in cert_info.items():
                setattr(cert, k, v)
                if k.startswith('remain_days'):
                    if int(v) <= 90:
                        certs_messages_remaind_email(cert, cert_info)
            cert.save()
        except  Exception as e:
            print(e)
        finally:
            Certs._meta.auto_created = False
    return 0
