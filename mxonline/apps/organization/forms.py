# coding:utf-8
__author__ = 'Dylan'

import re

from django import forms
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'course_name', 'phone']

    # def clean_phone(self):
    #     # phone_type = type(self.cleaned_data['phone'])
    #     mobile = self.cleaned_data['phone']
    #     regex = '^1[0-9]{10}'
    #     p = re.compile(regex)
    #     if p.match(str(mobile)):
    #         return mobile
    #     else:
    #         raise forms.ValidationError(u'手机号码格式不正确', code='phone number error')
