import requests
from requests.exceptions import ConnectionError

from PySELibrary import headers as headers_
from PySELibrary.core import ConnectionException


def connect(url, data=None, cookies=None, verify=None, headers=None, method="GET"):
    request = None
    try:
        if data is None:
            data = {}
        if headers is None:
            headers = headers_
        if method == "GET":
            request = requests.get(url,
                                   data,
                                   headers=headers,
                                   cookies=cookies,
                                   verify=verify)
        elif method == "POST":
            request = requests.post(url,
                                    data,
                                    headers=headers,
                                    cookies=cookies,
                                    verify=verify)
        return request
    except ConnectionError:
        raise ConnectionException


def get_cookies(url):
    return connect(url).cookies


def get_captcha(cookies):
    return requests.get("https://www.portal.nauta.cu/captcha/?", headers=headers_, cookies=cookies).content
