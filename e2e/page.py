import time
from selenium.common.exceptions import WebDriverException

from .urls import URL_CONF

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


class Urls:
    def __init__(self, url_dict, live_server_url):
        self.live_server_url = live_server_url
        if not isinstance(url_dict, dict):
            raise ValueError("url_dict type error {} instead of dict".format(type(url_dict)))
        self.url_dict = url_dict

    def __getattr__(self, item):
        url = self.url_dict.get(item, None)
        if url is None:
            raise KeyError('URL not found in dict')
        return "{server_url}{url}".format(server_url=self.live_server_url, url=url)


class Page:
    def __init__(self, browser_handle, live_server_url):
        self.browser = browser_handle
        self.urls = Urls(URL_CONF, live_server_url)

    @wait
    def get_login_email_field(self):
        return self.browser.find_element_by_id('id_username')

    @wait
    def get_login_password_field(self):
        return self.browser.find_element_by_id('id_password')

    @wait
    def get_login_checkbox(self):
        return self.browser.find_element_by_class_name('ui checkbox')

    @wait
    def get_login_submit_button(self):
        return self.browser.find_element_by_id('submit_button')

    @wait
    def find_error_messages_after_login_form_submission(self):
        return self.browser.find_element_by_css_selector('.ui.red.message')
