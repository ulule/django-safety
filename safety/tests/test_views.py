# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from safety.models import Session

from .base import BaseTestCase


class ViewsTest(BaseTestCase):
    def tearDown(self, *args, **kwargs):
        self.client.logout()

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

    def test_session_delete_view(self):
        admin_login_url = reverse('admin:login')
        session_list_url = reverse('safety:session_list')

        # Let's delete our current session.
        # We must be redirected to login page.

        self.login_user()
        session = Session.objects.first()

        r = self.client.post(reverse('safety:session_delete', kwargs={'pk': session.pk}), follow=True)
        self.assertRedirects(r, '%s?next=%s' % (admin_login_url, session_list_url))
        self.assertEqual(Session.objects.count(), 0)

        self.client.logout()

        # Let's delete an other session, not our current one.
        # We must be redirected to session list.

        fake_sessions = self.create_fake_sessions()
        self.assertEqual(Session.objects.count(), 10)

        self.login_user()

        sessions_count = Session.objects.count()
        self.assertEqual(sessions_count, 11)

        for session in fake_sessions:
            r = self.client.post(reverse('safety:session_delete', kwargs={'pk': session.pk}), follow=True)
            self.assertRedirects(r, session_list_url)

        self.assertEqual(Session.objects.count(), 1)

    def test_session_delete_other_view(self):
        session_list_url = reverse('safety:session_list')

        fake_sessions = self.create_fake_sessions()
        self.assertEqual(Session.objects.count(), 10)

        self.login_user()
        self.assertEqual(Session.objects.count(), 11)

        r = self.client.post(reverse('safety:session_delete_other'), follow=True)
        self.assertRedirects(r, session_list_url)
        self.assertEqual(Session.objects.count(), 1)
        current_session = Session.objects.get(session_key=self.client.session.session_key)

        r = self.client.get(reverse('safety:session_list'))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(self.client.session.exists(session_key=current_session.session_key))

        for session in fake_sessions:
            self.assertFalse(self.client.session.exists(session_key=session.session_key))
