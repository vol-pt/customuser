import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import logging

from .page import Page

logger = logging.getLogger(__name__)
DEFAULT_MAX_WAIT = 5


def wait(fn):
    def actual_decorator(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > DEFAULT_MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return actual_decorator


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        super(FunctionalTest, self).setUpClass()
        self.browser = webdriver.Chrome()

        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

        self.page = Page(self.browser, self.live_server_url)

    def tearDown(self):
        self.browser.quit()

    @wait
    def wait_for(self, fn):
        return fn()

    def wait_to_be_logged_in(self, email):
        self.wait_for(lambda: self.browser.find_element_by_link_text('Log out'))
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for(lambda: self.browser.find_element_by_name('email'))
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
