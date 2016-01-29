# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from .base import BaseTestCase

from safety.models import Session


class ViewsTest(BaseTestCase):
    
    def test_session_list_view(self):
        self.login_user()

        r = self.client.get(reverse('safety:session_list'))
        self.assertEqual(r.status_code, 200)

        objects = r.context['object_list']
        obj = r.context['object_list'][0]

        self.assertEqual(len(objects), 1)
        self.assertEqual(obj.user, self.user)
        self.assertTrue(obj.session_key)
        self.assertEqual(obj.ip, self.REMOTE_ADDR)
        self.assertEqual(obj.device, self.DEVICE)
        self.assertEqual(obj.location, self.LOCATION)

        self.client.logout()
