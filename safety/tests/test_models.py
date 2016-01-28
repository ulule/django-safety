# -*- coding: utf-8 -*-
from .base import BaseTestCase

from safety.models import Session


class ModelsTest(BaseTestCase):
    def test_create_session(self):
        self.assertEqual(Session.objects.count(), 0)
        self.client.login(username=self.user.username, password='secret')
        self.assertEqual(Session.objects.count(), 1)
