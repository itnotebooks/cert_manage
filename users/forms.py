#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 下午2:53
# @Version        : 1.0
# @File           : forms
# @Software       : PyCharm


from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'), max_length=100)
    password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput,
        max_length=128, strip=False
    )


class UserLoginCaptchaForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'), max_length=100)
    password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput,
        max_length=128, strip=False
    )
    captcha = CaptchaField()
