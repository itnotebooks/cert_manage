#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 上午7:03
# @Version        : 1.0
# @File           : views
# @Software       : PyCharm

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# 首页
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    session_week = None
    session_month = None
    session_month_dates = []
    session_month_dates_archive = []

    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(IndexView, self).get_context_data(**kwargs)
