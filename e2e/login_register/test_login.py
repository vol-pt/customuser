import time

from e2e.base import FunctionalTest

from selenium.webdriver.common.keys import Keys


class UserLoginTest(FunctionalTest):
    def test_unauthenticated_user_can_see_login_form(self):
        self.browser.get(self.page.urls.login)
        self.wait_for(lambda: self.page.get_login_email_field())
        self.wait_for(lambda: self.page.get_login_password_field())

    def test_unauthenticated_user_can_interact_with_form(self):
        self.browser.get(self.page.urls.login)

    def test_form_displays_error_message_on_incorrect_credentials(self):
        self.browser.get(self.page.urls.login)
        username = self.page.get_login_email_field()
        password = self.page.get_login_password_field()
        submit_button = self.page.get_login_submit_button()
        username.send_keys('doesnotexists@example.com')
        password.send_keys('weakgenericpassword123')
        submit_button.send_keys(Keys.ENTER)
        errors = self.page.find_error_messages_after_login_form_submission()
        self.assertIn('Invalid email or password', errors.text)

    def test_authenticated_user_is_redirected_to_user_profile(self):
        self.log_in_user('example@example.com', 'zaqmko321123')
        time.sleep(5)
        self.browser.get(self.page.urls.login)
        time.sleep(5)
        self.assertEqual(self.browser.current_url, self.page.urls.user_profile)
