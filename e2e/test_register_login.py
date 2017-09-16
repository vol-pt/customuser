from .base import FunctionalTest


class UserLoginTest(FunctionalTest):
    def test_unauthenticated_user_can_see_login_form(self):
        self.browser.get(self.live_server_url + '/login/')
        self.wait_for(lambda: self.page.get_login_email_field())
        self.wait_for(lambda: self.page.get_login_password_field())

    def test_unauthenticated_user_can_interact_with_form(self):
        self.browser.get()
