class Page:
    def __init__(self, browser_handle):
        self.browser = browser_handle

    def get_login_email_field(self):
        return self.browser.find_element_by_id('id_username')

    def get_login_password_field(self):
        return self.browser.find_element_by_id('id_password')
