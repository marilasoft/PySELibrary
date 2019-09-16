import requests
from requests.exceptions import ConnectionError

from PySELibrary import headers
from PySELibrary.core import ConnectionException


def connect(url, data=None, cookies=None, method="GET"):
    request = None
    try:
        if data is None:
            data = {}
        if method == "GET":
            request = requests.get(url,
                                   data,
                                   headers=headers,
                                   cookies=cookies)
        elif method == "POST":
            request = requests.post(url,
                                    data,
                                    headers=headers,
                                    cookies=cookies)
        return request
    except ConnectionError:
        raise ConnectionException


def get_cookies(url):
    return connect(url).cookies


def get_captcha(cookies):
    return requests.get("https://www.portal.nauta.cu/captcha/?", headers=headers, cookies=cookies).content
