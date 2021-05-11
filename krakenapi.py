import base64
import hashlib
import hmac
import os
import urllib.parse
from time import time

import requests as r
from dotenv import load_dotenv


class KrakenAPI:
    def __init__(self, pub_key=None, priv_key=None):
        load_dotenv()
        self.base_url = "https://api.kraken.com"
        if pub_key is None:
            self.pub_key = os.environ["KRAKEN_PUBLIC_KEY"]
        if priv_key is None:
            self.priv_key = os.environ["KRAKEN_PRIVATE_KEY"]

    def get_kraken_signature(urlpath, data, secret):

        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def _create_api_signature(self, urlpath: str, data: dict) -> str:
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(self.priv_key), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def _gen_nonce(self) -> str:
        return str(int(1000*time()))

    def _create_headers(self, endpoint: str, data: dict) -> dict:
        return {
            "API-Key": self.pub_key,
            "API-Sign": self._create_api_signature(endpoint, data)
        }

    def _create_data(self, **kwargs) -> dict:
        kwargs['nonce'] = self._gen_nonce()
        return {k: v for k, v in kwargs.items() if v is not None}

    def _send_req(self, endpoint: str, data: dict) -> r.Response:
        headers = self._create_headers(endpoint, data)
        return r.post(endpoint, headers=headers, data=data)

    def get_balance(self) -> r.Response:
        api_endpoint = self.base_url + "/0/private/Balance"
        data = self._create_data()
        print(data)
        return self._send_req(api_endpoint, data)

    def get_deposit_address(self, asset: str, method: str, new=True) -> r.Response:
        api_endpoint = self.base_url + "/0/private/DepositAddresses"
        data = self._create_data(asset=asset, method=method, new=new)
        return self._send_req(api_endpoint, data)

    def get_trade_balance(self, asset: str) -> r.Response:
        api_endpoint = self.base_url + "/0/private/TradeBalance"
        data = self._create_data(asset=asset)
        return self._send_req(api_endpoint, data)

    def get_open_orders(self, trades=False, userref=None) -> r.Response:
        api_endpoint = self.base_url + "/0/private/OpenOrders"
        data = self._create_data(trades=trades, userref=userref)
        return self._send_req(api_endpoint, data)

    def get_closed_orders(self, trades=False, userref=None, start=None, end=None, ofs=None, closetime="both"):
        api_endpoint = self.base_url + "/0/private/ClosedOrders"
        data = self._create_data(
            trades=trades, userref=userref, start=start, end=end, ofs=ofs, closetime=closetime)
        return self._send_req(api_endpoint, data)


if __name__ == "__main__":
    api = KrakenAPI()
    print(api.pub_key)
    print(api.priv_key)
    print(api.get_balance().json())
