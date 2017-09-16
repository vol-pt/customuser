import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import logging

from .page import Page, wait

logger = logging.getLogger(__name__)


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        super(FunctionalTest, self).setUpClass()
        self.browser = webdriver.Firefox()

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
