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

from users.models import User, UserGroup


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


class UserCreateUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput,
        max_length=128, strip=False, required=False,
    )

    class Meta:
        model = User
        fields = [
            'username', 'name', 'email', 'groups', 'phone', 'role', 'date_expired', 'comment'
        ]
        help_texts = {
            'username': '* required',
            'name': '* required',
            'email': '* required',
        }
        widgets = {
            'groups': forms.SelectMultiple(
                attrs={
                    'class': 'select2',
                    'data-placeholder': _('Join user groups')
                }
            )
        }

    # 重写init方法
    def __init__(self, initial, *args, **kwargs):
        super(UserCreateUpdateForm, self).__init__(*args, **kwargs)
        self.fields['roles_checkbox'].initial = False

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        user = super().save(commit=commit)

        if password:
            user.set_password(password)
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'name', 'email', 'phone',
        ]
        help_texts = {
            'username': '* required',
            'name': '* required',
            'email': '* required',
        }


UserProfileForm.verbose_name = _("Profile")


class UserPasswordForm(forms.Form):
    old_password = forms.CharField(
        max_length=128, widget=forms.PasswordInput,
        label=_("Old password")
    )
    new_password = forms.CharField(
        min_length=5, max_length=128,
        widget=forms.PasswordInput,
        label=_("New password")
    )
    confirm_password = forms.CharField(
        min_length=5, max_length=128,
        widget=forms.PasswordInput,
        label=_("Confirm password")
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.instance.check_password(old_password):
            raise forms.ValidationError(_('Old password error'))
        return old_password

    def clean_confirm_password(self):
        new_password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_password']

        if new_password != confirm_password:
            raise forms.ValidationError(_('Password does not match'))
        return confirm_password

    def save(self):
        password = self.cleaned_data['new_password']
        self.instance.set_password(password)
        self.instance.save()
        return self.instance


class UserGroupForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label=_("User"),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'select2',
                'data-placeholder': _('Select users')
            }
        ),
        required=False,
    )

    def __init__(self, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', {})
            initial.update({
                'users': instance.users.all(),
            })
            kwargs['initial'] = initial
        super().__init__(**kwargs)

    def save(self, commit=True):
        group = super().save(commit=commit)
        users = self.cleaned_data['users']
        group.users.set(users)
        return group

    class Meta:
        model = UserGroup
        fields = [
            'name', 'users', 'comment'
        ]
        help_texts = {
            'name': '* required'
        }
