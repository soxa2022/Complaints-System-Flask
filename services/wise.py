import uuid
import requests
from decouple import config


class WiseService(object):
    SOURCE_CURRENCY = "EUR"
    TARGET_CURRENCY = "EUR"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {config('WISE_TOKEN')}",
            "Content-Type": "application/json",
        }
        self.base_url = config("BASE_URL")
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self):
        url = f"{config('BASE_URL')}/v2/profiles"
        response = requests.get(url, headers=self.headers)
        return response.json()[0]["id"]

    def create_quote(self, amount):
        url = f"{config('BASE_URL')}/v3/profiles/{self.profile_id}/quotes"
        body = {
            "sourceCurrency": self.SOURCE_CURRENCY,
            "targetCurrency": self.TARGET_CURRENCY,
            "sourceAmount": amount,
        }
        response = requests.post(url, json=body, headers=self.headers)
        return response.json()["id"]

    def create_recipient(self, full_name, iban):
        url = f"{config('BASE_URL')}/v1/accounts"
        body = {
            "currency": self.TARGET_CURRENCY,
            "type": "iban",
            "profile": self.profile_id,
            "ownedByCustomer": False,
            "accountHolderName": full_name,
            "details": {
                "legalType": "PRIVATE",
                "IBAN": iban,
            },
        }
        response = requests.post(url, json=body, headers=self.headers)
        return response.json()["id"]

    def create_transfer(self, quote_id, recipient_id, custom_trans_id):
        url = f"{config('BASE_URL')}/v1/transfers"
        body = {
            "targetAccount": recipient_id,
            "quoteUuid": quote_id,
            "customerTransactionId": custom_trans_id,
            "details": {
                "reference": "return money",
                "transferPurpose": "approved complaint",
            },
        }
        response = requests.post(url, json=body, headers=self.headers)
        return response.json()["id"]

    def fund_transfer(self, transfer_id):
        url = f"{config('BASE_URL')}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"
        body = {"type": "BALANCE"}

        response = requests.post(url, json=body, headers=self.headers)
        return response

    def cancel_transfers(self, transfer_id):
        url = f"{config('BASE_URL')}/v1/transfers/{transfer_id}/cancel"
        response = requests.put(url, json=None, headers=self.headers)
        return response


# if __name__ == "__main__":
#     wise = WiseService()
#     custom_trans_id = str(uuid.uuid4())
#     quote_id = wise.create_quote(200)
#     recipient_id = wise.create_recipient("Anton Ivanov", "BG80BNBG96611020345678")
#     transfer_id = wise.create_transfer(quote_id, recipient_id, custom_trans_id)
