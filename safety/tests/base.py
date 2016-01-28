# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from exam.cases import Exam
from exam.decorators import fixture


UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) '
      'AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 '
      'Safari/536.26.17')


class Fixtures(Exam):
    @fixture
    def user(self):
        return User.objects.create_superuser(
            username='johndoe',
            email='johndoe@example.com',
            password='secret')


class BaseTestCase(Fixtures, TestCase):
    def login_user(self):
        admin_login_url = reverse('admin:login')
        self.client.post(
            admin_login_url,
            data={
                'username': self.user.username,
                'password': 'secret',
                'next': '/admin/'},
                REMOTE_ADDR='127.0.0.1',
                HTTP_USER_AGENT=UA)
