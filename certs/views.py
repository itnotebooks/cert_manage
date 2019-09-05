from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView

from django.utils.translation import ugettext as _

from users.utils import create_success_msg
from cert_manage.utils import AdminUserRequiredMixin

from certs import forms
from certs.models import Certs


# Create your views here.


class CertListView(AdminUserRequiredMixin, TemplateView):
    """
    列出所有证书
    """
    template_name = 'cert/cert_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Cert'),
            'action': _('List')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class CertCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    '''
    创建证书
    '''
    model = Certs
    form_class = forms.CertCreateUpdateForm
    template_name = 'cert/cert_create_update.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    # 重写get_form_kwargs，在initial中传入参数pk
    def get_form_kwargs(self):
        kwargs = super(CertCreateView, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        kwargs['initial']['pk'] = False
        return kwargs

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Cert'),
            'action': _('Create'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_success_message(self, cleaned_data):
        return create_success_msg % ({"name": cleaned_data["name"]})

    def get_success_url(self):
        return reverse_lazy('certs:cert-index')


class CertUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    '''
    更新证书
    '''
    model = Certs
    form_class = forms.CertCreateUpdateForm
    template_name = 'cert/cert_create_update.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form

    # 重写get_form_kwargs，在initial中传入参数pk
    def get_form_kwargs(self):
        kwargs = super(CertUpdateView, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        kwargs['initial']['pk'] = self.kwargs.get('pk')
        return kwargs

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Cert'),
            'action': _('Update'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_success_message(self, cleaned_data):
        return create_success_msg % ({"name": cleaned_data["name"]})

    def get_success_url(self):
        return reverse_lazy('certs:cert-index')


class CertDetailView(AdminUserRequiredMixin, DetailView):
    '''
    证书详细信息
    '''
    model = Certs
    context_object_name = 'cert'
    template_name = 'cert/cert_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Cert'),
            'action': _('Detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
