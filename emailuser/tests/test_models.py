from django.test import TestCase
from ..models import EmailUser as EmailUser


class EmailUserTest(TestCase):
    def test_get_short_name_returns_email(self):
        user = EmailUser.objects.create(email='test@example.com', password='12345678910abcd')
        self.assertEqual(user.email, 'test@example.com')

    def test_get_full_name_returns_email(self):
        user = EmailUser.objects.create(email='test@example.com', password='12345678910abcd')
        self.assertEqual(user.email, 'test@example.com')

