import os

import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import logging

from selenium.webdriver.common.keys import Keys

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

    def log_in_user(self, email, password):
        # register
        self.browser.get(self.page.urls.register)
        email_ = self.page.get_register_email()
        password1 = self.page.get_register_password_1()
        password2 = self.page.get_register_password_2()
        gender = self.page.get_register_select_gender()
        birth_date = self.page.get_register_birth_date()

        email_.send_keys(email)
        password1.send_keys(password)
        password2.send_keys(password)
        password2.send_keys(Keys.TAB)
        time.sleep(0.5)  # wait for js animation
        gender.send_keys(Keys.ARROW_DOWN)
        gender.send_keys(Keys.ENTER)
        time.sleep(0.5)  # wait for js animation
        gender.send_keys(Keys.TAB)

        time.sleep(0.5)  # wait for js animation
        birth_date.send_keys(Keys.ENTER)
        birth_date.send_keys(Keys.ENTER)
        birth_date.send_keys(Keys.ENTER)
        # log in with enter
        self.page.click_on_tos()
        email_.send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector('.ui.positive.message'))