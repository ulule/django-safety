# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from exam.cases import Exam
from exam.decorators import fixture

from safety.models import Session


class Fixtures(Exam):
    UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) '
          'AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 '
          'Safari/536.26.17')

    DEVICE = 'Safari 6.0.2 - Mac OS X 10.8.2'
    LOCATION = 'Mountain View, United States'
    REMOTE_ADDR = '66.249.64.0'

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
                'next': '/admin/',
            },
            REMOTE_ADDR=self.REMOTE_ADDR,
            HTTP_USER_AGENT=self.UA)

    def create_fake_sessions(self):
        sessions = []
        for x in range(10):
            self.client.session.save()
            session = Session.objects.create(
                user=self.user,
                session_key=self.client.session.session_key,
                ip=self.REMOTE_ADDR,
                location=self.LOCATION,
                device=self.DEVICE,
                user_agent=self.UA,
                expire_date=self.client.session.get_expiry_date())
            sessions.append(session)
        return sessions
