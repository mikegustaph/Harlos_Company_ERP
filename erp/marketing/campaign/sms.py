import requests
# import gevent
import schedule
# from gevent import monkey
from cachetools import cached, TTLCache


class SendSMS(object):
    """
    A Module to send SMS using OPES BULK SMS
    """

    def __init__(self):
        self.apikey_url = "http://solutions.opestechnologies.co.tz/api/get-api-key"
        self.sendsms_url = "http://solutions.opestechnologies.co.tz/api/messages/send"
        self.get_balance_url = (
            "http://solutions.opestechnologies.co.tz/api/messages/get-balance"
        )

    @cached(cache=TTLCache(maxsize=1024, ttl=864_000))
    def api_key(self) -> str:
        try:
            token = requests.post(
                self.apikey_url, json={
                    "name": "Harlos", "password": "Harlos@2019"}
            ).json()

            if token.get("error"):
                print("The invalid username/password used")
                return
            return token["success"]["token"]

        except (requests.ConnectTimeout, requests.ConnectionError):
            raise ConnectionError

    def get_default_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key()}",
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0",
        }

    @property
    @cached(cache=TTLCache(maxsize=1024, ttl=1200))
    def get_balance(self) -> dict:
        try:
            print("Trying something")
            response = requests.get(
                self.get_balance_url,
                headers=self.get_default_headers(),
                timeout=2,
                verify=False,
            )
            print("Request processed")
            if response.status_code == 200:
                return response.json()["balance"]
            return 0
        except Exception as bug:
            print("Failed")
            print(bug)
            return 0

    @staticmethod
    def format_the_number(mobile: str) -> str:
        mobile = str(mobile)
        if isinstance(mobile, str):
            if mobile.startswith("0"):
                mobile = "255" + mobile[1:]
                return mobile
            elif mobile.startswith("+"):
                mobile = mobile[1:]
                return mobile
            elif mobile.startswith("255"):
                return mobile
            else:
                print(mobile)
                raise TypeError("Please format your number in (255) xxxxxx")
        else:
            print(mobile)
            print(type(mobile))
            raise TypeError(
                f"Mobile number should be string not {type(mobile)}")

    def send_sms(self, message: str, mobile_no: str) -> bool:
        try:

            mobile_no = str(mobile_no)

            print(mobile_no)

            print(f"Sending to {self.format_the_number(mobile_no)}")

            sendsms_query = {
                "messages": [
                    {
                        "sender": "Harlos Cont",
                        "channel": "6600",
                        "text": message,
                        "msisdn": self.format_the_number(mobile_no),
                        "msg_id": "",
                    }
                ]
            }

            return requests.post(
                self.sendsms_url,
                json=sendsms_query,
                headers=self.get_default_headers(),
                verify=True,
            )

        except (requests.ConnectTimeout, requests.ConnectionError):
            raise ConnectionError

    def send_bulk(self, message: str, contacts: list, contact_names: list = []) -> bool:
        try:

            if isinstance(message, str) and isinstance(contacts, list):
                for contact in contacts:
                    self.send_sms(message=str(message), mobile_no=str(contact))
                return True
            return False

        except Exception as bug:
            print(bug)
            return False
