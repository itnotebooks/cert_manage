from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.cache import cache
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.urls import reverse

from django.utils.decorators import method_decorator

from django.utils.translation import ugettext as _

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView

from users import forms
from users.utils import redirect_user_first_login_or_index, set_tmp_user_to_cache, get_login_ip, get_user_or_tmp_user


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
            'interval': 5,
            'redirect_url': reverse('index'),
            'auto_redirect': True,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
