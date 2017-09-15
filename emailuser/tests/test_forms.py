from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.shortcuts import reverse
from ..forms import EmailUserAuthenticationForm
from ..models import EmailUser as EmailUser
from .base import BaseEmailUserTest


class LoginFormTest(BaseEmailUserTest):
    def setUp(self):
        self.factory = RequestFactory()

    def test_form_renders_correct_html(self):
        form = EmailUserAuthenticationForm()
        self.assertIn('input type="email" name="username"', form.as_p())
        self.assertIn('input type="password" name="password"', form.as_p())
        self.assertIn('input type="checkbox" name="remember_me"', form.as_p())

    def test_form_is_valid_without_remember_me_checkbox(self):
        EmailUser.objects.create_user(email='test210@example.com', password='zaqmko123123')
        form = EmailUserAuthenticationForm(data={'username': 'test210@example.com', 'password': 'zaqmko123123'})
        form.request = self.build_dummy_request_with_session_handling()
        self.assertTrue(form.is_valid())
