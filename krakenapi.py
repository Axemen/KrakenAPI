import base64
import hashlib
import hmac
import os
import urllib.parse
from time import time
from typing import Union

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

    # Utils
    def _create_api_signature(self, urlpath: str, data: dict) -> str:
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(self.priv_key),
                       message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def _gen_nonce(self) -> str:
        return str(int(1000*time()))

    def _create_headers(self, endpoint: str, data: dict) -> dict:
        return {
            "API-Key": "M6qUu7ezzlMLIo87QeW9Ssj7/lx8l1KlhvDoZ0rTOarSJ0u13FKPDTob",
            "API-Sign": self._create_api_signature(endpoint, data)
        }

    def _create_data(self, **kwargs) -> dict:
        kwargs['nonce'] = self._gen_nonce()
        return {k: v for k, v in kwargs.items() if v is not None}

    def _send_req(self, endpoint: str, data: dict) -> r.Response:
        headers = self._create_headers(endpoint, data)
        return r.post(self.base_url + endpoint, headers=headers, data=data)

    # User Data
    def get_account_balance(self) -> r.Response:
        api_endpoint = "/0/private/Balance"
        data = self._create_data()
        print(data)
        return self._send_req(api_endpoint, data)

    def get_trade_balance(self, asset: str) -> r.Response:
        api_endpoint = "/0/private/TradeBalance"
        data = self._create_data(asset=asset)
        return self._send_req(api_endpoint, data)

    def get_open_orders(self, trades: bool = False, userref: Union[int, None] = None) -> r.Response:
        api_endpoint = "/0/private/OpenOrders"
        data = self._create_data(trades=trades, userref=userref)
        return self._send_req(api_endpoint, data)

    def get_closed_orders(self, trades: bool = False, userref: Union[int, None] = None, start: int = None, end: int = None, ofs: int = None, closetime: str = "both"):
        api_endpoint = "/0/private/ClosedOrders"
        data = self._create_data(
            trades=trades, userref=userref, start=start, end=end, ofs=ofs, closetime=closetime)
        return self._send_req(api_endpoint, data)

    def query_orders_info(self, txid: str, trades: bool = False, userref: Union[int, None] = None):
        api_endpoint = "/0/private/QueryOrders"
        data = self._create_data(txid=txid, trades=trades, userref=userref)
        return self._send_req(api_endpoint, data)

    def get_trades_history(self, type: str = "all", trades: bool = False, start: Union[int, None] = None, end: Union[int, None] = None, ofs: Union[int, None] = None):
        api_endpoint = "/0/private/TradesHistory"
        data = self._create_data(
            type=type, trades=trades, start=start, end=end, ofs=ofs)
        return self._send_req(api_endpoint, data)

    def query_trades_info(self, txid: str, trades: bool = False):
        api_endpoint = "/0/private/QueryTrades"
        data = self._create_data(txid=txid, trades=trades)
        return self._send_req(api_endpoint, data)

    def get_open_positions(self, txid: Union[str, None] = None, docalcs: bool = False, consolidation: str = 'market'):
        api_endpoint = "/0/private/OpenPositions"
        data = self._create_data(
            txid=txid, docalcs=docalcs, consolidation=consolidation)
        return self._send_req(api_endpoint, data)

    def get_ledgers_info(self, asset: str = 'all', aclass: str = 'currency', type: str = 'all', start: Union[int, None] = None, end: Union[int, None] = None, ofs: Union[int, None] = None):
        api_endpoint = "/0/private/Ledgers"
        data = self._create_data(
            asset=asset, aclass=aclass, type=type, start=start, end=end, ofs=ofs)
        return self._send_req(api_endpoint, data)

    def query_ledgers(self, id: Union[str, None] = None, trades: bool = False):
        api_endpoint = "/0/private/QueryLedgers"
        data = self._create_data(id=id, trades=trades)
        return self._send_req(api_endpoint, data)

    def get_trade_volume(self, pair: str, fee_info: bool = False):
        api_endpoint = "/0/private/TradeVolume"
        data = self._create_data(pair=pair, fee_info=fee_info)
        return self._send_req(api_endpoint, data)

    def request_export_report(self, report: str, description: str, format: str = 'csv', fields: str = 'all', starttm: Union[int, None] = None, endtm: Union[int, None] = None):
        api_endpoint = "/0/private/AddExport"
        data = self._create_data(report=report, description=description,
                                 format=format, fields=fields, starttm=starttm, endtm=endtm)
        return self._send_req(api_endpoint, data)

    def get_export_reqort_status(self, report: str):
        api_endpoint = "/0/private/ExportStatus"
        data = self._create_data(report=report)
        return self._send_req(api_endpoint, data)

    def retrieve_data_export(self, id: str):
        api_endpoint = "/0/private/RetrieveExport"
        data = self._create_data(id=id)
        return self._send_req(api_endpoint, data)

    def delete_export_report(self, id: str, type: str):
        api_endpoint = "/0/private/RemoveExport"
        data = self._create_data(id=id, type=type)
        return self._send_req(api_endpoint, data)

    # User Trading
    def add_order(self, ordertype: str, type: str, pair: str, **kwargs):
        """ 
        [required]
        ordertype
        type
        pair
        [optional arguments]
        userref: int        
        volume:str
        price:str
        price2:str
        leverage:str
        oflags:str
        starttm:str
        expiretm:str
        close_order_type (close[ordertype]): str
        close_price (close[price])
        close_price2 (close[price2])
        trading_agreement
        validate
        """
        # The person who wrote these parameters to have brackets in them is a fucking maniac
        api_endpoint = "/0/private/AddOrder"
        data = self._create_data(
            ordertype=ordertype, type=type, pair=pair).update(kwargs)

        # I fucking hate this endpoint in particular
        if "close_order_type" in data:
            data['close[ordertype]'] = data["close_order_type"]
            del data['close_order_type']
        if "close_price" in data:
            data['close[price]'] = data["close_price"]
            del data['close_price']
        if "close_price2" in data:
            data['close[price2]'] = data['close_price2']
            del data['close_price2']

        return self._send_req(api_endpoint, data)

    def cancel_order(self, txid: Union[str, int]):
        api_endpoint = "/0/private/CancelOrder"
        data = self._create_data(txid=txid)
        return self._send_req(api_endpoint, data)

    def cancel_all_orders(self):
        api_endpoint = "/0/private/CancelAll"
        data = self._create_data()
        return self._send_req(api_endpoint, data)

    def cancel_all_orders_after_x(self, timeout: int):
        api_endpoint = "/0/private/CancelAllOrdersAfter"
        data = self._create_data(timeout=timeout)
        return self._send_req(api_endpoint, data)

    # User Funding

    def get_deposit_methods(self, asset: str):
        api_endpoint = "/0/private/DepositMethods"
        data = self._craete_data(asset=asset)
        return self._send_req(api_endpoint, data)

    def get_deposit_address(self, asset: str, method: str, new: bool = True) -> r.Response:
        api_endpoint = "/0/private/DepositAddresses"
        data = self._create_data(asset=asset, method=method, new=new)
        return self._send_req(api_endpoint, data)

    def get_status_of_recent_deposits(self, asset: str, method: Union[str, None] = None):
        api_endpoint = "/0/private/DepositStatus"
        data = self._create_data(asset=asset, method=method)
        return self._send_req(api_endpoint, data)

    def get_withdrawl_information(self, asset: str, key: str, amount: str):
        api_endpoint = '/0/private/WithdrawInfo'
        data = self._create_data(asset=asset, key=key, amount=amount)
        return self._send_req(api_endpoint, data)

    def withdrawl_funds(self, asset: str, key: str, amount: str):
        api_endpoint = '/0/private/Withdraw'
        data = self._create_data(asset=asset, key=key, amount=amount)
        return self._send_req(api_endpoint, data)

    def get_status_of_recent_withdrawls(self, asset: str, method: Union[str, None] = None):
        api_endpoint = '/0/private/WithdrawStatus'
        data = self._create_data(asset=asset, method=method)
        return self._send_req(api_endpoint, data)

    def request_withdrawl_cancelation(self, asset: str, refid: str):
        api_endpoint = "/0/private/WithdrawCancel"
        data = self._create_data(asset=asset, refid=refid)
        return self._send_req(api_endpoint, data)

    def request_wallet_transfer(self, asset: str, _from: str, to: str, amount: str):
        api_endpoint = "/0/private/WalletTransfer"
        data = self._create_data(asset=asset, to=to, amount=amount)
        data['from'] = _from
        return self._send_req(api_endpoint, data)

    def get_websocket_token(self):
        api_endpoint = "/0/private/GetWebSocketsToken"
        data = self._create_data()
        return self._send_req(api_endpoint, data)

    # Market data
    def get_server_time(self):
        return r.get(self.base_url + '/0/public/Time')

    def get_system_status(self):
        return r.get(self.base_url + "/0/public/SystemStatus")

    def get_asset_info(self, asset: Union[str, None] = None, aclass: Union[str, None] = None):
        api_endpoint = "/0/public/Assets?"

        params = {}
        if asset is not None:
            params['asset'] = asset
        if aclass is not None:
            params['aclass'] = aclass

        if params:
            params = urllib.parse.urlencode(params)
            return r.get(self.base_url + api_endpoint + params)
        return r.get(self.base_url + api_endpoint)

    def get_tradable_asset_pairs(self, pair: Union[str, None] = None, info: str = 'info'):
        api_endpoint = "/0/public/AssetPairs?"
        params = {}
        if pair is not None:
            params['pair'] = pair
        params['info'] = info
        params = urllib.parse.urlencode(params)
        return r.get(self.base_url + api_endpoint + params)

    def get_ticker_info(self, pair: str):
        api_endpoint = f"/0/public/Ticker?pair={pair}"
        return r.get(self.base_url + api_endpoint)

    def get_ohlc(self, pair: str, interval: int = 1, since: Union[int, None] = None):
        api_endpoint = "/0/public/OHLC?"
        params = {
            'pair': pair,
            'interval': interval
        }
        if since is not None:
            params['since'] = since
        params = urllib.parse.urlencode(params)
        return r.get(self.base_url + api_endpoint + params)

    def get_order_book(self, pair: str, count: Union[int, None] = None):
        api_endpoint = "/0/public/Depth?"
        params = {"pair": pair}
        if count is not None:
            params['count'] = count
        params = urllib.parse.urlencode(params)
        return r.get(self.base_url + api_endpoint + params)

    def get_recent_trades(self, pair: str, since: Union[str, None] = None):
        api_endpoint = "/0/public/Trades?"
        params = {"pair": pair}
        if since is not None:
            params['since'] = since
        params = urllib.parse.urlencode(params)
        return r.get(self.base_url + api_endpoint + params)

    def get_recent_spreads(self, pair: str, since: Union[int, None] = None):
        api_endpoint = "/0/public/Spread?"
        params = {"pair": pair}
        if since is not None:
            params['since'] = since
        params = urllib.parse.urlencode(params)
        return r.get(self.base_url + api_endpoint + params)


if __name__ == "__main__":
    api = KrakenAPI()
    print(api.get_recent_spreads('BTC/USD').json())
