from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse


class BaseEmailUserTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def build_dummy_request_with_session_handling(self):
        dummy_request = self.factory.get(reverse('login'))
        session_middleware = SessionMiddleware()
        session_middleware.process_request(dummy_request)
        dummy_request.session.save()
        return dummy_request
