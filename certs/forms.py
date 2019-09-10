#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-5 上午9:01
# @Version        : 1.0
# @File           : forms
# @Software       : PyCharm


from django import forms
from django.utils.translation import ugettext_lazy as _

from certs.models import Certs
from users.models import User


class CertCreateUpdateForm(forms.ModelForm):
    is_domain = forms.BooleanField(initial=True, required=False, help_text=_('域名或证书文件'),
                                   label='is_domain')

    class Meta:
        model = Certs
        fields = [
            'name', 'method', 'domain_url', 'crt_file', 'key_file', 'users', 'comment'
        ]

        widgets = {
            'domain_url': forms.TextInput(
                attrs={
                    'placeholder': _('通用名称')
                }
            ),
            'users': forms.SelectMultiple(attrs={
                'class': 'select2',
                'data-placeholder': _('选择用户')
            }),
        }

        help_texts = {
            'name': '* required',
            'domain_url': 'eg: www.itnotebooks.com',
        }

    # 重写init方法
    def __init__(self, initial, *args, **kwargs):
        super(CertCreateUpdateForm, self).__init__(*args, **kwargs)
        if initial.get('pk'):
            cert = Certs.objects.get(id=initial.get('pk'))
            if int(cert.method) == 1:
                self.fields['is_domain'].initial = False

    # 重写save方法，处理多个字段的问题
    def save(self, commit=True):
        certs = super().save(commit=commit)
        if not self.cleaned_data.get('is_domain'):
            certs.method = 1
            certs.save()
        return certs
