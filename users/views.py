import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.urls import reverse_lazy, reverse

from django.utils.decorators import method_decorator

from django.utils.translation import ugettext as _

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView, UpdateView, CreateView, DetailView

from users import forms
from users.models import User, UserGroup
from users.signals import post_user_create

from users.utils import redirect_user_first_login_or_index, set_tmp_user_to_cache, get_login_ip, get_user_or_tmp_user, \
    create_success_msg, update_success_msg

from cert_manage.utils import AdminUserRequiredMixin


# Create your views here.

@method_decorator(sensitive_post_parameters(), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class UserLoginView(FormView):
    template_name = 'users/login.html'
    form_class = forms.UserLoginForm
    form_class_captcha = forms.UserLoginCaptchaForm
    redirect_field_name = 'next'
    key_prefix = "_LOGIN_INVALID_{}"

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect(self.get_success_url())
        request.session.set_test_cookie()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if not self.request.session.test_cookie_worked():
            return HttpResponse(_("Please enable cookies and try again."))

        set_tmp_user_to_cache(self.request, form.get_user())
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        ip = get_login_ip(self.request)
        cache.set(self.key_prefix.format(ip), 1, 3600)
        old_form = form
        form = self.form_class_captcha(data=form.data)
        form._errors = old_form.errors
        return super().form_invalid(form)

    def get_form_class(self):
        ip = get_login_ip(self.request)
        if cache.get(self.key_prefix.format(ip)):
            return self.form_class_captcha
        else:
            return self.form_class

    def get_success_url(self):
        user = get_user_or_tmp_user(self.request)
        auth_login(self.request, user)
        return redirect_user_first_login_or_index(self.request, self.redirect_field_name)

    def get_context_data(self, **kwargs):
        context = {
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


@method_decorator(never_cache, name='dispatch')
class UserLogoutView(TemplateView):
    template_name = 'flash_message_standalone.html'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Logout success'),
            'messages': _('Logout success, return login page'),
            'interval': 1,
            'redirect_url': reverse('index'),
            'auto_redirect': True,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'users/user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'app': _('Users'),
            'action': _('User list'),
        })
        return context


class UserCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = forms.UserCreateUpdateForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('users:user-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'app': _('Users'),
                        'action': _('Create user')
                        })
        return context

    def form_valid(self, form):
        user = form.save(commit=True)

        post_user_create.send(self.__class__, user=user)
        return super().form_valid(form)


class UserUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = forms.UserCreateUpdateForm
    template_name = 'users/user_update.html'
    context_object_name = 'user_object'
    success_url = reverse_lazy('users:user-list')
    success_message = update_success_msg

    def get_context_data(self, **kwargs):
        context = {'app': _('Users'),
                   'action': _('Update user'),
                   }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserDetailView(AdminUserRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = "user_object"

    def get_context_data(self, **kwargs):
        groups = UserGroup.objects.exclude(id__in=self.object.groups.all())

        context = {
            'app': _('Users'),
            'action': _('User detail'),
            'groups': groups
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserProfileView(LoginRequiredMixin, TemplateView):
    # model = User
    template_name = 'users/user_profile.html'

    # context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = {
            'action': _('Profile')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/user_profile_update.html'
    model = User
    form_class = forms.UserProfileForm
    success_url = reverse_lazy('users:user-profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = {
            'app': _('User'),
            'action': _('Profile setting'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserPasswordUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/user_password_update.html'
    model = User
    form_class = forms.UserPasswordForm
    success_url = reverse_lazy('users:user-profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('Password update'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        auth_logout(self.request)
        return super().get_success_url()


class UserGroupListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'users/user_group_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('User group list')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupDetailView(AdminUserRequiredMixin, DetailView):
    model = UserGroup
    context_object_name = 'user_group'
    template_name = 'users/user_group_detail.html'

    def get_context_data(self, **kwargs):
        users = User.objects.exclude(id__in=self.object.users.all())
        context = {
            'app': _('Users'),
            'action': _('User group detail'),
            'users': users,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = UserGroup
    form_class = forms.UserGroupForm
    template_name = 'users/user_group_create_update.html'
    success_url = reverse_lazy('users:user-group-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('Create user group'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserGroup
    form_class = forms.UserGroupForm
    template_name = 'users/user_group_create_update.html'
    success_url = reverse_lazy('users:user-group-list')
    success_message = update_success_msg

    def get_context_data(self, **kwargs):
        users = User.objects.all()
        group_users = [user.id for user in self.object.users.all()]
        context = {
            'app': _('Users'),
            'action': _('Update user group'),
            'users': users,
            'group_users': group_users
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
