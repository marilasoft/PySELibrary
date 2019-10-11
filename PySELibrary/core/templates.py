from datetime import datetime


class Connection(object):

    def __init__(self, **kwargs):
        self.start_session = kwargs["start_session"]
        self.end_session = kwargs["end_session"]
        self.duration = kwargs["duration"]
        self.upload = kwargs["upload"]
        self.download = kwargs["download"]
        self.import_ = kwargs["import_"]

    @property
    def start_session_as_dt(self):
        date_ = self.start_session.split(" ")[0]
        time_ = self.start_session.split(" ")[1]

        day = date_.split("/")[0]
        month = date_.split("/")[1]
        year = date_.split("/")[2]

        hours = time_.split(":")[0]
        minutes = time_.split(":")[1]
        seconds = time_.split(":")[2]

        return datetime(int(year), int(month), int(day),
                        int(hours), int(minutes), int(seconds))


class Recharge(object):

    def __init__(self, **kwargs):
        self.date = kwargs["date"]
        self.import_ = kwargs["import_"]
        self.channel = kwargs["channel"]
        self.type_ = kwargs["type_"]

    @property
    def date_as_dt(self):
        date_ = self.date.split(" ")[0]
        time_ = self.date.split(" ")[1]

        day = date_.split("/")[0]
        month = date_.split("/")[1]
        year = date_.split("/")[2]

        hours = time_.split(":")[0]
        minutes = time_.split(":")[1]
        seconds = time_.split(":")[2]

        return datetime(int(year), int(month), int(day),
                        int(hours), int(minutes), int(seconds))


class Transfer(object):

    def __init__(self, **kwargs):
        self.date = kwargs["date"]
        self.import_ = kwargs["import_"]
        self.destiny_account = kwargs["destiny_account"]

    @property
    def date_as_dt(self):
        date_ = self.date.split(" ")[0]
        time_ = self.date.split(" ")[1]

        day = date_.split("/")[0]
        month = date_.split("/")[1]
        year = date_.split("/")[2]

        hours = time_.split(":")[0]
        minutes = time_.split(":")[1]
        seconds = time_.split(":")[2]

        return datetime(int(year), int(month), int(day),
                        int(hours), int(minutes), int(seconds))


class Product(object):

    def __init__(self, product):
        self.product = product

    @property
    def title(self):
        return self.product.find_all("h4")[0].text

    @property
    def description(self):
        return self.product.find_all("div", {"class": "offerPresentationProductDescription_msdp product_desc"})[0] \
            .find_all("span")[0].text

    @property
    def price(self):
        return self.product.find_all("div", {"class": "offerPresentationProductDescription_msdp product_desc"})[0] \
                   .find_all("span", {"class": "bold"})[0].text + " CUC"

    @property
    def actions(self):
        actions = {}
        actions_ = self.product.find_all("div", {"class": "offerPresentationProductBuyAction_msdp ptype"})[0]
        actions["mostInfo"] = actions_.find_all("a", {"class": "offerPresentationProductBuyLink_msdp"})[0] \
            .attrs["href"]
        actions["buy"] = actions_ \
            .find_all("a", {"class": "offerPresentationProductBuyLink_msdp button_style link_button"})[0] \
            .attrs["href"]
        return actions
