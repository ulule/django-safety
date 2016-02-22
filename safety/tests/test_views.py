# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from safety.forms import PasswordChangeForm
from safety.models import PasswordChange, Session

from .base import BaseTestCase


class SessionsViewsTest(BaseTestCase):
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
        self.assertTrue(obj.active)
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


class PasswordChangeViewsTest(BaseTestCase):
    def test_password_change(self):
        self.login_user()

        r = self.client.get(reverse('safety:password_change'))
        self.assertTemplateUsed(r, 'safety/password_change/form.html')
        self.assertEqual(r.status_code, 200)

        self.client.logout()

    def test_password_change_done(self):
        self.login_user()

        r = self.client.get(reverse('safety:password_change_done'))
        self.assertTemplateUsed(r, 'safety/password_change/done.html')
        self.assertEqual(r.status_code, 200)

        self.client.logout()

    def test_workflow(self):
        change_form_url = reverse('safety:password_change')

        # We don't have any PasswordChange instance yet.
        # Because we just plugged the app.
        self.assertEqual(PasswordChange.objects.count(), 0)

        # Let's login user.
        self.login_user()

        # We still have no instance.
        self.assertEqual(PasswordChange.objects.count(), 0)

        # Let's create an instance for a given user.
        # By default, "required" field is set to False.
        # So nothing changes.
        pr, created = PasswordChange.objects.get_or_create_for_user(self.user)
        self.assertTrue(created)
        self.assertFalse(pr.required)

        # Let's logout user and login again, than go elsewhere
        # on the site. As we don't set required to True yet,
        # nothing changes again.
        self.client.logout()
        self.login_user()

        r = self.client.get(reverse('home'))
        self.assertEqual(r.status_code, 200)

        r = self.client.get(reverse('admin:index'))
        self.assertEqual(r.status_code, 200)

        # Time to force user to reset its password.
        pr.required = True
        pr.save()

        # Now, it should be effictive because we use the decorator
        # (the middleware or the decorator provides the same behavior).
        # So we must be redirected to password change form. No other choice.
        r = self.client.get(reverse('home'))
        self.assertRedirects(r, change_form_url)

        r = self.client.get(reverse('admin:index'))
        self.assertRedirects(r, change_form_url)

        # Now, ok. User is stuck. Time to change password.
        # Let's change password!

        r = self.client.post(
            reverse('safety:password_change'),
            data={
                'old_password': self.USER_PASSWORD,
                'new_password1': 'superpassword',
                'new_password2': 'superpassword',
            })

        self.assertRedirects(r, reverse('safety:password_change_done'))

        # Done. New password.
        #
        # A few days later, we required user to change its password again.
        # But! We do not accept the old one again. User must provide a
        # different new password. Let's check it.
        pr, created = PasswordChange.objects.get_or_create_for_user(self.user)
        self.assertFalse(created)

        # As we changed our last password, required field must be now set to False.
        self.assertFalse(pr.required)

        # Let's switch.
        pr.required = True
        pr.save()

        # Login with new password.
        self.login_user(password='superpassword')

        # Boom! Redirected.
        r = self.client.get(reverse('home'))
        self.assertRedirects(r, change_form_url)

        # Let's reload our fixture.
        self.reload()

        # Let's try to reset our password with the same as old one.
        r = self.client.post(
            reverse('safety:password_change'),
            data={
                'old_password': 'superpassword',
                'new_password1': 'superpassword',
                'new_password2': 'superpassword',
            })

        # Boom! Error. Not authorized.
        self.assertFormError(r, 'form', 'new_password2', PasswordChangeForm.error_messages['same_password'])

        # OK. Choose a new one.
        r = self.client.post(
            reverse('safety:password_change'),
            data={
                'old_password': 'superpassword',
                'new_password1': 'ournewpassword',
                'new_password2': 'ournewpassword',
            })

        # Everything is OK.
        self.assertRedirects(r, reverse('safety:password_change_done'))

        # Login with new password.
        self.login_user(password='ournewpassword')

        # No redirect. Everything is OK.
        r = self.client.get(reverse('home'))
        self.assertEqual(r.status_code, 200)
