# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from .base import BaseTestCase

from safety.models import Session


class ViewsTest(BaseTestCase):
    def test_session_list_view(self):
        self.login_user()

        r = self.client.get(reverse('safety:session_list'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['object_list']), 1)

        obj = r.context['object_list'][0]
        self.assertEqual(obj.user, self.user)
        self.assertTrue(obj.session_key)
        self.assertEqual(obj.ip, '127.0.0.1')
        self.assertEqual(obj.device, 'Safari 6.0.2 - Mac OS X 10.8.2')

        self.client.logout()
