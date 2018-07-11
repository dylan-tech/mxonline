# coding:utf-8
__author__ = 'Dylan'

import random
import string

from users.models import EmailVerityCode
from django.core.mail import send_mail
from mxonline.settings import EMAIL_FROM


def random_str(random_num=8):
    str = ''
    charset = string.digits + string.letters
    random_range = len(charset) - 1
    for i in range(random_num):
        new_str = random.randint(0, random_range)
        str += charset[new_str]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerityCode()
    code = random_str(16)
    email_record.email = email
    email_record.code = code
    email_record.send_type = send_type
    email_record.save()
    if send_type == 'register':
        title = u'慕学在线学习注册激活链接'
        body = u'请点击下面的链接以激活该用户账号:http://127.0.0.1:8000/active/{0}'.format(code)
        send_mail(title, body, EMAIL_FROM, [email])
    elif send_type == 'forget':
        title = u'慕学在线学习重置密码链接'
        body = u'请点击下面的链接以重置密码:http://127.0.0.1:8000/reset/{0}'.format(code)
        send_mail(title, body, EMAIL_FROM, [email])


