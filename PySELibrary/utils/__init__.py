import re

from bs4 import BeautifulSoup


def find_error(page, _type="UP"):
    if _type is "IP":
        replace_text = "\r\n       \talert"
        replace_text_one = '\r\n       \talert("'
        replace_text_two = '");\r\n   \t'
    else:
        replace_text = "toastr.error"
        replace_text_one = "toastr.error('"
        replace_text_two = "');"
    errors = []
    try:
        script = page.find_all("script", {"type": "text/javascript"})[-1]
        if script.text.startswith(replace_text):
            text = script.text.replace(replace_text_one, "").replace(replace_text_two, "")
            if _type is "IP":
                return text
            html = BeautifulSoup(text, "html.parser")
            error = html.find_all("li", {"class": "msg_error"})[0]
            if error.text.startswith("Se han detectado algunos errores."):
                sub_messages = error.find_all("li", {"class": "sub-message"})
                for sub_message in sub_messages:
                    errors.append(sub_message.text)
            else:
                errors.append(error.text)
        return errors
    except IndexError:
        return ["Error Desconocido"]


def find_success(page):
    script = page.find_all("script", {"type": "text/javascript"})[-1]
    if script.text.startswith("toastr.success"):
        text = script.text.replace("toastr.success('", "").replace("');", "")
        html = BeautifulSoup(text, "html.parser")
        return html.find("li", {"class": "msg_message"}).text


def get_session_info(page):
    script = page.find_all("script", {"type": "text/javascript"})[0]
    text_temp = script.text.split("/EtecsaQueryServlet?")
    text_temp1 = text_temp[1].split('", true);')
    params_in_brut = text_temp1[0].split("&")
    session_info = {}
    for param in params_in_brut:
        session_info[param.split("=")[0]] = param.split("=")[1]

    return session_info


def url_logout(page):
    script = page.find_all("script", {"type": "text/javascript"})[0]
    attribute_uuid_re = "ATTRIBUTE_UUID=(.*\")"
    str2 = re.findall(attribute_uuid_re, script.text)[0].replace("\"", "")
    wlanuserip_re = "wlanuserip=(.*\")"
    str3 = re.findall(wlanuserip_re, script.text)[0].replace("\"", "")
    logger_id_re = "loggerId=(.*\")"
    str4 = re.findall(logger_id_re, script.text)[0].replace("\"", "")
    username_re = "username=(.*\")"
    str5 = re.findall(username_re, script.text)[0].replace("\"", "")
    str1_re = "CSRFHW=(.*&)"
    str1 = re.findall(str1_re, script.text)[0]
    return "/LogoutServlet?CSRFHW=%sATTRIBUTE_UUID=%s&wlanuserip=%s&ssid=&loggerId=%s&domain=&username=%s&wlanacname=" \
           "&wlanmac=&remove=1" % (str1, str2, str3, str4, str5)
