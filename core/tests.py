from django.test import TestCase
from .models import CustomUser
from django.utils import timezone


class LoginTest(TestCase):
    def test_can_log_in(self):
        user = CustomUser.objects.create_user('kami1234l@wp.pl', '12345678910kamil', date_of_birth=timezone.now())
        self.client.login(email='kami1234l@wp.pl', password='12345678910kamil')
        response = self.client.get('/', follow=True)
        self.assertContains(response, 'Logout')
        self.assertContains(response, 'Hello {username}'.format(username=user.email))
