# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now

from exam.cases import Exam
from exam.decorators import fixture

from safety.models import Session
from safety.utils import get_session_store


class Fixtures(Exam):
    UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) '
          'AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 '
          'Safari/536.26.17')

    DEVICE = 'Safari 6.0.2 - Mac OS X 10.8.2'
    LOCATION = 'Mountain View, United States'
    REMOTE_ADDR = '66.249.64.0'
    USER_PASSWORD = 'secret'

    @fixture
    def user(self):
        return User.objects.create_superuser(
            username='johndoe',
            email='johndoe@example.com',
            password=self.USER_PASSWORD)

    def reload(self):
        self.user = User.objects.get(pk=self.user.pk)


class BaseTestCase(Fixtures, TestCase):
    def login_user(self, password=None):
        admin_login_url = reverse('admin:login')
        password = password or self.USER_PASSWORD

        self.client.post(
            admin_login_url,
            data={
                'username': self.user.username,
                'password': password,
                'next': '/admin/',
            },
            REMOTE_ADDR=self.REMOTE_ADDR,
            HTTP_USER_AGENT=self.UA)

    def create_fake_sessions(self):
        store = get_session_store()

        sessions = []
        for x in range(10):
            store.create()
            session = Session.objects.create(
                user=self.user,
                session_key=store.session_key,
                ip=self.REMOTE_ADDR,
                location=self.LOCATION,
                device=self.DEVICE,
                user_agent=self.UA,
                last_activity=now(),
                expiration_date=store.get_expiry_date())
            sessions.append(session)

        return sessions
