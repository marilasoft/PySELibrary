APP_NAME = "PySELibrary"
VERSION = "0.0.1-r0.3"
DESCRIPTION = "Interactua con los servicios web de ETECSA."
KEYWORDS = "ETECSA nauta tools"
AUTHOR_NAME = "lesclaz"
AUTHOR_EMAIL = "lesclaz95@gmail.com"
URL = "https://gitlab.home.asr/marilasoft/PySELibrary"
LICENSE = "GNU GPLv3"
LONG_DESCRIPTION = "PySELibrary fue creada para la Comunidad Android de Cuba, para facilitar el desarrollo de " \
                   "aplicaciones en Python que interactúen con el Portal de Usuario y el Portal Cautivo de nauta; " \
                   "así como el Portal Mi Cubacel, ahorrándoles tiempo, esfuerzos, neuronas y código a los " \
                   "desarrolladores."

url_list = {"base": "https://www.portal.nauta.cu/",
            "login": "https://www.portal.nauta.cu/user/login/es-es",
            "user_info": "https://www.portal.nauta.cu/useraaa/user_info",
            "recharge": "https://www.portal.nauta.cu/useraaa/recharge_account",
            "transfer": "https://www.portal.nauta.cu/useraaa/transfer_balance",
            "service_detail": "https://www.portal.nauta.cu/useraaa/service_detail",
            "service_detail_summary": "https://www.portal.nauta.cu/useraaa/service_detail_summary",
            "service_detail_list": "https://www.portal.nauta.cu/useraaa/service_detail_list/",
            "recharge_detail": "https://www.portal.nauta.cu/useraaa/recharge_detail/",
            "recharge_detail_summary": "https://www.portal.nauta.cu/useraaa/recharge_detail_summary/",
            "recharge_detail_list": "https://www.portal.nauta.cu/useraaa/recharge_detail_list/",
            "transfer_detail": "https://www.portal.nauta.cu/useraaa/transfer_detail/",
            "transfer_detail_summary": "https://www.portal.nauta.cu/useraaa/transfer_detail_summary/",
            "transfer_detail_list": "https://www.portal.nauta.cu/useraaa/transfer_detail_list/",
            "logout": "https://www.portal.nauta.cu/user/logout",
            "change_password": "https://www.portal.nauta.cu/useraaa/change_password",
            "change_email_password": "https://www.portal.nauta.cu/email/change_password",
            "captive_portal_login": "https://secure.etecsa.net:8443/",
            "captive_portal_login_action": "https://secure.etecsa.net:8443//LoginServlet",
            "captive_portal_user_info": "https://secure.etecsa.net:8443/EtecsaQueryServlet",
            "captive_portal_terms_of_use": "https://secure.etecsa.net:8443/nauta_etecsa/LoginURL/pc"
                                           "/pc_termsofuse.jsp",
            "captive_portal_online_do": "https://secure.etecsa.net:8443/web/online.do?"
                                        "CSRFHW=f28fea085dfdf24fbbd2f2b7c12581e9&",
            "captive_protal_get_time": "https://secure.etecsa.net:8443/EtecsaQueryServlet",
            "captive_portal_base_url": "https://secure.etecsa.net:8443"}

headers = {"user-agent": "%s/%s" % (APP_NAME, VERSION)}

from datetime import date

from bs4 import BeautifulSoup

from .core import ChangePasswordException
from .core import Connection
from .core import GetInfoException
from .core import LoginException
from .core import Recharge
from .core import RechargeException
from .core import Transfer
from .net import connect
from .net import get_captcha
from .net import get_cookies
from .utils import find_error
from .utils import find_success
from .utils import get_session_info
from .utils import url_logout


class UserPortal(object):

    def __init__(self):
        self.cookies = None
        self.csrf = None
        self.captcha_img = None
        self.page = None
        self.status = None

    def load_captcha(self, cookies):
        self.captcha_img = get_captcha(cookies)

    def get_csrf(self, url, cookies):
        self.page = BeautifulSoup(connect(url, cookies=cookies).text, "html.parser")
        _input = self.page.find("input", {"name": "csrf"})
        self.csrf = _input.attrs["value"]

    def load_login(self, cookies):
        self.get_csrf(url_list["login"], cookies)

    def pre_login(self):
        self.cookies = get_cookies(url_list["login"])
        self.load_login(self.cookies)

    def get_csrf_login(self, cookies):
        self.get_csrf(url_list["login"], cookies)

    def reload_user_info(self, cookies):
        self.page = BeautifulSoup(connect(url_list["user_info"], cookies=cookies).text, "html.parser")

    def login(self, user_name, password, captcha_code, cookies):
        data = {"csrf": self.csrf,
                "login_user": user_name,
                "password_user": password,
                "captcha": captcha_code,
                "btn_submit": ""}
        self.page = BeautifulSoup(connect(url_list["login"], data, cookies, method="POST").text, "html.parser")

        if find_error(self.page):
            errors = find_error(self.page)
            self.status = {"status": "error",
                           "msg": errors}
            raise LoginException(errors)
        else:
            self.status = {"status": "success",
                           "msg": find_success(self.page)}

    def recharge(self, recharge_code, cookies):
        self.get_csrf(url_list["recharge"], cookies)
        data = {"csrf": self.csrf,
                "recharge_code": recharge_code,
                "btn_submit": ""}
        self.page = BeautifulSoup(connect(url_list["recharge"], data, cookies, method="POST").text, "html.parser")

        if find_error(self.page):
            errors = find_error(self.page)
            self.status = {"status": "error",
                           "msg": errors}
            raise RechargeException(errors)
        else:
            self.status = {"status": "success",
                           "msg": find_success(self.page)}

    def transfer(self, mount_to_transfer, account_to_transfer, password_user, cookies):
        self.get_csrf(url_list["transfer"], cookies)
        data = {"csrf": self.csrf,
                "transfer": mount_to_transfer,
                "password_user": password_user,
                "id_cuenta": account_to_transfer,
                "action": "checkdata"}
        self.page = BeautifulSoup(connect(url_list["transfer"], data, cookies, method="POST").text, "html.parser")

        if find_error(self.page):
            errors = find_error(self.page)
            self.status = {"status": "error",
                           "msg": errors}
            raise RechargeException(errors)
        else:
            self.status = {"status": "success",
                           "msg": find_success(self.page)}

    def change_password(self, old_password, new_password, cookies):
        self.get_csrf(url_list["change_password"], cookies)
        data = {"csrf": self.csrf,
                "old_password": old_password,
                "new_password": new_password,
                "repeat_new_password": new_password,
                "btn_submit": ""}
        self.page = BeautifulSoup(connect(url_list["change_password"], data, cookies, method="POST").text,
                                  "html.parser")

        if find_error(self.page):
            errors = find_error(self.page)
            self.status = {"status": "error",
                           "msg": errors}
            raise ChangePasswordException(errors)
        else:
            self.status = {"status": "success",
                           "msg": find_success(self.page)}

    def change_email_password(self, old_password, new_password, cookies):
        self.get_csrf(url_list["change_email_password"], cookies)
        data = {"csrf": self.csrf,
                "old_password": old_password,
                "new_password": new_password,
                "repeat_new_password": new_password,
                "btn_submit": ""}
        self.page = BeautifulSoup(connect(url_list["change_email_password"], data, cookies, method="POST").text,
                                  "html.parser")

        if find_error(self.page):
            errors = find_error(self.page)
            self.status = {"status": "error",
                           "msg": errors}
            raise ChangePasswordException(errors)
        else:
            self.status = {"status": "success",
                           "msg": find_success(self.page)}

    def get_last_connections(self, cookies):
        connections = []
        today = date.today()
        if today.month <= 9:
            year_month = "%s-0%s" % (today.year, today.month)
        else:
            year_month = "%s-%s" % (today.year, today.month)
        connections.extend(self.get_connections(year_month, cookies))
        if len(connections) < 5:
            if today.month == 1:
                month = 12
                connections.extend(self.get_connections("%s-%s" % (today.year - 1, month), cookies))
                if len(connections) < 5:
                    connections.extend(self.get_connections("%s-%s" % (today.year - 1, month - 1), cookies))
            else:
                connections.extend(self.get_connections("%s-%s" % (today.year, today.month - 1), cookies))
                if len(connections) < 5:
                    if today.month - 1 == 1:
                        month = 12
                        connections.extend(self.get_connections("%s-%s" % (today.year - 1, month), cookies))
                    else:
                        connections.extend(self.get_connections("%s-%s" % (today.year, today.month - 2), cookies))
        if len(connections) > 5:
            return self.order(connections)
        else:
            return connections

    @staticmethod
    def order(connections):
        for i, a in enumerate(connections):
            for e, b in enumerate(connections):
                if i > e:
                    pass
                else:
                    if connections[i].start_session_as_dt < connections[e].start_session_as_dt:
                        temp = connections[i]
                        connections[i] = connections[e]
                        connections[e] = temp
        return [connections[0], connections[1],
                connections[2], connections[3],
                connections[4]]

    def get_connections(self, year_month, cookies):
        self.get_csrf(url_list["service_detail"], cookies)
        data = {"csrf": self.csrf,
                "year_month": year_month,
                "list_type": "service_detail"}
        self.page = BeautifulSoup(connect(url_list["service_detail_list"] +
                                          year_month, data, cookies, method="POST").text,
                                  "html.parser")
        connections = []

        table = self.page.find("table", {"class": "striped bordered highlight responsive-table"})
        try:
            trs = table.find_all("tr")
            trs.pop(0)
            for tr in trs:
                tds = tr.find_all("td")
                connections.append(Connection(start_session=tds[0].text,
                                              end_session=tds[1].text,
                                              duration=tds[2].text,
                                              upload=tds[3].text,
                                              download=tds[4].text,
                                              import_=tds[5].text))
        except AttributeError:
            pass

        if len(connections) == 0:
            self.page = BeautifulSoup(connect(url_list["service_detail_summary"], data, cookies, method="POST").text,
                                      "html.parser")

            if find_error(self.page):
                errors = find_error(self.page)
                self.status = {"status": "error",
                               "msg": errors}
                raise GetInfoException(errors)
            else:
                self.status = {"status": "success",
                               "msg": find_success(self.page)}

        return connections

    def get_recharges(self, year_month, cookies):
        self.get_csrf(url_list["recharge_detail"], cookies)
        data = {"csrf": self.csrf,
                "year_month": year_month,
                "list_type": "recharge_detail"}
        self.page = BeautifulSoup(connect(url_list["recharge_detail_list"] +
                                          year_month, data, cookies, method="POST").text,
                                  "html.parser")
        recharges = []

        table = self.page.find("table", {"class": "striped bordered highlight responsive-table"})
        try:
            trs = table.find_all("tr")
            trs.pop(0)
            for tr in trs:
                tds = tr.find_all("td")
                recharges.append(Recharge(date=tds[0].text,
                                          import_=tds[1].text,
                                          channel=tds[2].text,
                                          type_=tds[3].text))
        except AttributeError:
            pass

        if len(recharges) == 0:
            self.page = BeautifulSoup(connect(url_list["recharge_detail_summary"], data, cookies, method="POST").text,
                                      "html.parser")

            if find_error(self.page):
                errors = find_error(self.page)
                self.status = {"status": "error",
                               "msg": errors}
                raise GetInfoException(errors)
            else:
                self.status = {"status": "success",
                               "msg": find_success(self.page)}

        return recharges

    def get_transfers(self, year_month, cookies):
        self.get_csrf(url_list["transfer_detail"], cookies)
        data = {"csrf": self.csrf,
                "year_month": year_month,
                "list_type": "transfer_detail"}
        self.page = BeautifulSoup(connect(url_list["transfer_detail_list"] +
                                          year_month, data, cookies, method="POST").text,
                                  "html.parser")
        transfers = []

        table = self.page.find("table", {"class": "striped bordered highlight responsive-table"})
        try:
            trs = table.find_all("tr")
            trs.pop(0)
            for tr in trs:
                tds = tr.find_all("td")
                transfers.append(Transfer(date=tds[0].text,
                                          import_=tds[1].text,
                                          destiny_account=tds[2].text))
        except AttributeError:
            pass

        if len(transfers) == 0:
            self.page = BeautifulSoup(connect(url_list["transfer_detail_summary"], data, cookies, method="POST").text,
                                      "html.parser")

            if find_error(self.page):
                errors = find_error(self.page)
                self.status = {"status": "error",
                               "msg": errors}
                raise GetInfoException(errors)
            else:
                self.status = {"status": "success",
                               "msg": find_success(self.page)}

        return transfers

    def logout(self, cookies):
        self.page = BeautifulSoup(connect(url_list["logout"], cookies).text, "html.parser")
        if find_error(self.page)[0] == "El usuario debe estar registrado para realizar esta operación.":
            self.status = {"status": "success",
                           "msg": "La session fue cerrada correctamente!"}

    def __get_attr__(self, attr):
        divs = self.page.find_all("div", {"class": "col s12 m6"})
        for div in divs:
            h5 = div.find("h5")
            if h5.text == attr:
                credit = div.find("p")
                return credit.text

    @property
    def user_name(self):
        return self.__get_attr__("Usuario ")

    @property
    def block_date(self):
        return self.__get_attr__("Fecha de bloqueo")

    @property
    def delete_date(self):
        return self.__get_attr__("Fecha de eliminación")

    @property
    def account_type(self):
        return self.__get_attr__("Tipo de cuenta")

    @property
    def service_type(self):
        return self.__get_attr__("Tipo de servicio ")

    @property
    def credit(self):
        return self.__get_attr__("Saldo disponible")

    @property
    def time(self):
        return self.__get_attr__("Tiempo disponible de la cuenta")

    @property
    def mail_account(self):
        return self.__get_attr__("Cuenta de correo")


class CaptivePortal(object):

    def __init__(self):
        self.cookies = None
        self.page = None
        self.status = None
        self.terms_of_use = []
        self.user_info = {"status": "",
                          "credit": "",
                          "expire": "",
                          "access_areas": ""}
        self.session_info = {}

        self.wlanuserip = None
        self.wlanacname = None
        self.wlanmac = None
        self.firsturl = None
        self.ssid = None
        self.usertype = None
        self.gotopage = None
        self.successpage = None
        self.loggerId = None
        self.lang = None
        self.CSRFHW = None

    def get_info_pre_login(self, url, cookies):
        self.page = BeautifulSoup(connect(url, cookies=cookies).text, "html.parser")

        _input = self.page.find("input", {"name": "wlanuserip"})
        self.wlanuserip = _input.attrs["value"]

        _input = self.page.find("input", {"name": "wlanacname"})
        self.wlanacname = _input.attrs["value"]

        _input = self.page.find("input", {"name": "wlanmac"})
        self.wlanmac = _input.attrs["value"]

        _input = self.page.find("input", {"name": "firsturl"})
        self.firsturl = _input.attrs["value"]

        _input = self.page.find("input", {"name": "ssid"})
        self.ssid = _input.attrs["value"]

        _input = self.page.find("input", {"name": "usertype"})
        self.usertype = _input.attrs["value"]

        _input = self.page.find("input", {"name": "gotopage"})
        self.gotopage = _input.attrs["value"]

        _input = self.page.find("input", {"name": "successpage"})
        self.successpage = _input.attrs["value"]

        _input = self.page.find("input", {"name": "loggerId"})
        self.loggerId = _input.attrs["value"]

        _input = self.page.find("input", {"name": "lang"})
        self.lang = _input.attrs["value"]

        _input = self.page.find("input", {"name": "CSRFHW"})
        self.CSRFHW = _input.attrs["value"]

    def pre_login(self):
        self.cookies = get_cookies(url_list["captive_portal_login"])
        self.get_info_pre_login(url_list["captive_portal_login"], self.cookies)

    def login(self, user_name, password, cookies):
        data = {"wlanuserip": self.wlanuserip,
                "wlanacname": self.wlanacname,
                "wlanmac": self.wlanmac,
                "firsturl": self.firsturl,
                "ssid": self.ssid,
                "usertype": self.usertype,
                "gotopage": self.gotopage,
                "successpage": self.successpage,
                "loggerId": self.loggerId,
                "lang": self.lang,
                "username": user_name,
                "password": password,
                "CSRFHW": self.CSRFHW}
        self.page = BeautifulSoup(connect(url_list["captive_portal_login_action"], data, cookies, method="POST").text,
                                  "html.parser")
        a = open("la", "w")
        a.write(str(self.page))
        a.close()
        if find_error(self.page, _type="IP"):
            self.status = {"status": "error",
                           "msg": find_error(self.page, _type="IP")}
            raise LoginException(self.status["msg"])

    def update_available_time(self, cookies):
        return connect(url_list["captive_protal_get_time"],
                       get_session_info(self.page),
                       cookies).text

    def logout(self, cookies):
        logout_page = BeautifulSoup(connect(url_list["captive_portal_base_url"] + url_logout(self.page), cookies).text,
                                    "html.parser")
        if logout_page.text.replace("logoutcallback('", "").replace("');", "") != "SUCCESS":
            raise LoginException(self.status["msg"])

    def get_user_info(self, user_name, password, cookies):
        data = {"wlanuserip": self.wlanuserip,
                "wlanacname": self.wlanacname,
                "wlanmac": self.wlanmac,
                "firsturl": self.firsturl,
                "ssid": self.ssid,
                "usertype": self.usertype,
                "gotopage": self.gotopage,
                "successpage": self.successpage,
                "loggerId": self.loggerId,
                "lang": self.lang,
                "username": user_name,
                "password": password,
                "CSRFHW": self.CSRFHW}
        self.page = BeautifulSoup(connect(url_list["captive_portal_user_info"], data, cookies, method="POST").text,
                                  "html.parser")

        if find_error(self.page, _type="IP"):
            self.status = {"status": "error",
                           "msg": find_error(self.page, _type="IP")}
            raise LoginException(self.status["msg"])

        table = self.page.find("table", {"id": "sessioninfo"})

        try:
            trs = table.find_all("tr")
            self.user_info["status"] = trs[0].find_all("td")[1].text \
                .replace("\r\n\t\t\t\t\t\t\t\t\t\t\t", "") \
                .replace("\r\n\t\t\t\t\t\t\t\t\t\t", "")
            self.user_info["credit"] = trs[1].find_all("td")[1].text \
                .replace("\r\n\t\t\t\t\t\t\t\t\t\t\t", "") \
                .replace("\r\n\t\t\t\t\t\t\t\t\t\t", "")
            self.user_info["expire"] = trs[2].find_all("td")[1].text \
                .replace("\r\n\t\t\t\t\t\t\t\t\t\t\t", "") \
                .replace("\r\n\t\t\t\t\t\t\t\t\t\t", "")
            self.user_info["access_areas"] = trs[3].find_all("td")[1].text \
                .replace("\r\n\t\t\t\t\t\t\t\t\t\t\t", "") \
                .replace("\r\n\t\t\t\t\t\t\t\t\t\t", "")
        except AttributeError:
            pass

    def get_terms_of_use(self, cookies):
        data = {"wlanuserip": self.wlanuserip,
                "wlanacname": self.wlanacname,
                "wlanmac": self.wlanmac,
                "firsturl": self.firsturl,
                "ssid": self.ssid,
                "usertype": self.usertype,
                "gotopage": self.gotopage,
                "successpage": self.successpage,
                "loggerId": self.loggerId,
                "lang": self.lang,
                "username": "",
                "password": "",
                "CSRFHW": self.CSRFHW}
        self.page = BeautifulSoup(connect(url_list["captive_portal_terms_of_use"], data, cookies, method="POST").text,
                                  "html.parser")

        if find_error(self.page, _type="IP"):
            self.status = {"status": "error",
                           "msg": find_error(self.page, _type="IP")}
            raise LoginException(self.status["msg"])

        ol = self.page.find("ol", {"class": "condiciones"})

        try:
            terms = ol.find_all("li")
            for term in terms:
                self.terms_of_use.append(term.text)
        except AttributeError:
            pass
