from kraken_api import KRAKEN_BASE_URL
import urllib
import hashlib
import hmac
import base64
from time import time
import os

import requests as r


def _create_api_signature(urlpath: str, data: dict) -> str:
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(os.environ["KRAKEN_PRIVATE_KEY"]),
                   message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


def _gen_nonce() -> str:
    return str(int(1000*time()))


def _create_headers(endpoint: str, data: dict) -> dict:
    return {
        "API-Key": os.environ["KRAKEN_PUBLIC_KEY"],
        "API-Sign": _create_api_signature(endpoint, data)
    }


def _create_data(**kwargs) -> dict:
    kwargs['nonce'] = _gen_nonce()
    return {k: v for k, v in kwargs.items() if v is not None}


def _send_req(endpoint: str, data: dict) -> r.Response:
    headers = _create_headers(endpoint, data)
    return r.post(KRAKEN_BASE_URL + endpoint, headers=headers, data=data)
