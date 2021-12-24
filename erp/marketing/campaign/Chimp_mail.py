import re
import requests
from mailchimp_marketing import Client
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError


class SendMail(object):
    def __init__(self):
        self.api_key = "92cef284506a0c4e854ba4ca94aabeb9-us7"
        self.sever_url = "us7"
        self.mailchimp_client = self.get_client
        self.email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

    @property
    def get_client(self):
        try:
            mailchimp = Client()
            mailchimp.set_config({"api_key": self.api_key, "server": self.sever_url})
            response = mailchimp.ping.get()
            print(response)
            return mailchimp
        except (requests.ConnectTimeout, requests.ConnectionError):
            raise ConnectionError("Ping failed, please check your network")

    def add_an_adience(
        self,
        audience_email: str,
    ):
        try:
            pass

        except (requests.ConnectTimeout, requests.ConnectionError):
            raise ConnectionError(
                "Adding contacts faileds, Please check your internet connection"
            )

    def send_mail(self, email_body, email) -> bool:
        try:
            pass

        except (requests.ConnectTimeout, requests.ConnectionError):
            raise ConnectionError(
                "Failed to send an email, Please check your internet connection"
            )

    def bulk_mail(self, email_body: str, customer_emails: list, names: list = []):
        try:
            for email in customer_emails:
                if re.search(self.email_regex, email):
                    self.send_mail(email=email, email_body=email_body)
                    continue
                print(f"{email} is not a valid email")
        except Exception as bug:
            print(bug)
            return
