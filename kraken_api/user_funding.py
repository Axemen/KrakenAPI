from typing import Union

import requests as r

from .utils import _create_data, _send_req


def get_deposit_methods( asset: str):
    api_endpoint = "/0/private/DepositMethods"
    data = _create_data(asset=asset)
    return _send_req(api_endpoint, data)


def get_deposit_address( asset: str, method: str, new: bool = True) -> r.Response:
    api_endpoint = "/0/private/DepositAddresses"
    data = _create_data(asset=asset, method=method, new=new)
    return _send_req(api_endpoint, data)


def get_status_of_recent_deposits( asset: str, method: Union[str, None] = None):
    api_endpoint = "/0/private/DepositStatus"
    data = _create_data(asset=asset, method=method)
    return _send_req(api_endpoint, data)


def get_withdrawl_information( asset: str, key: str, amount: str):
    api_endpoint = '/0/private/WithdrawInfo'
    data = _create_data(asset=asset, key=key, amount=amount)
    return _send_req(api_endpoint, data)


def withdrawl_funds( asset: str, key: str, amount: str):
    api_endpoint = '/0/private/Withdraw'
    data = _create_data(asset=asset, key=key, amount=amount)
    return _send_req(api_endpoint, data)


def get_status_of_recent_withdrawls( asset: str, method: Union[str, None] = None):
    api_endpoint = '/0/private/WithdrawStatus'
    data = _create_data(asset=asset, method=method)
    return _send_req(api_endpoint, data)


def request_withdrawl_cancelation( asset: str, refid: str):
    api_endpoint = "/0/private/WithdrawCancel"
    data = _create_data(asset=asset, refid=refid)
    return _send_req(api_endpoint, data)


def request_wallet_transfer( asset: str, _from: str, to: str, amount: str):
    api_endpoint = "/0/private/WalletTransfer"
    data = _create_data(asset=asset, to=to, amount=amount)
    data['from'] = _from
    return _send_req(api_endpoint, data)


def get_websocket_token():
    api_endpoint = "/0/private/GetWebSocketsToken"
    data = _create_data()
    return _send_req(api_endpoint, data)
