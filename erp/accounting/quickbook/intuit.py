import time
import json
import datetime
from typing import List, Dict
from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects.customer import Customer


class Intuit(object):
    def __init__(self) -> None:
        self.api = self.create_intuit_api()

    def create_intuit_api(self):
        intuit_auth = AuthClient(
            client_id="AB5yppq7VLOQdRtIHeyyFoP2pz2iXiNDIVRR3vsY0n4emHmUuH",
            client_secret="KjSl5spbKLG5igZLL8GDJA00KbIos9AJTwrPpWju",
            environment="sandbox",
            redirect_uri="http://localhost:5000/accounting",
        )

        return QuickBooks(
            auth_client=intuit_auth,
            refresh_token="AB11621174028QjIESmpQ8n068MBeIWtF8gartffeYHZtXl8M5",
            company_id=" 4620816365161075480",
        )

    def load_customer(self, customer_name):
        try:
            customer = Customer()
            return customer.query("select * from Customer", qb=self.api)
        except TypeError as bug:
            print("Failed to create new customer")
            print(bug)
            return False
