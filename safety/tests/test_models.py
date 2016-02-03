# -*- coding: utf-8 -*-
from .base import BaseTestCase

from safety.models import (
    PasswordReset,
    Session,
)


class ModelsTest(BaseTestCase):
    def tearDown(self, *args, **kwargs):
        super(ModelsTest, self).tearDown(*args, **kwargs)

        self.client.logout()

    def test_session(self):
        self.assertEqual(Session.objects.count(), 0)

        self.login_user()
        self.assertEqual(Session.objects.count(), 1)

    def test_password_reset(self):
        self.assertEqual(PasswordReset.objects.count(), 0)

        self.login_user()
        self.assertEqual(PasswordReset.objects.count(), 1)

        obj = PasswordReset.objects.first()

        self.assertEqual(obj.user, self.user)
        self.assertIsNone(obj.last_reset_date)
        self.assertEqual(obj.last_password, self.user.password)
        self.assertFalse(obj.required)

        self.user.set_password('foo')
        self.user.save()

        self.login_user(password='foo')

        obj = PasswordReset.objects.first()

        self.assertEqual(obj.user, self.user)
        self.assertIsNotNone(obj.last_reset_date)
        self.assertEqual(obj.last_password, self.user.password)
        self.assertFalse(obj.required)
