from .urls import URL_CONF


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

    def get_login_email_field(self):
        return self.browser.find_element_by_id('id_username')

    def get_login_password_field(self):
        return self.browser.find_element_by_id('id_password')
