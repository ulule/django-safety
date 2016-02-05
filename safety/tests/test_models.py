# -*- coding: utf-8 -*-
from .base import BaseTestCase

from safety.models import (
    PasswordChange,
    Session,
)


class ModelsTest(BaseTestCase):
    def test_session(self):
        self.assertEqual(Session.objects.count(), 0)
        self.login_user()
        self.assertEqual(Session.objects.count(), 1)
        self.client.logout()

    def test_password_change(self):
        obj, created = PasswordChange.objects.get_or_create_for_user(self.user)
        self.assertTrue(created)
        self.assertEqual(obj.user, self.user)
        self.assertIsNone(obj.last_change_date)
        self.assertFalse(obj.required)
