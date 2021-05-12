import requests as r
from typing import Union
import urllib
from .__init__ import KRAKEN_BASE_URL

def get_server_time():
    return r.get(KRAKEN_BASE_URL + '/0/public/Time')

def get_system_status():
    return r.get(KRAKEN_BASE_URL + "/0/public/SystemStatus")

def get_asset_info( asset: Union[str, None] = None, aclass: Union[str, None] = None):
    api_endpoint = "/0/public/Assets?"

    params = {}
    if asset is not None:
        params['asset'] = asset
    if aclass is not None:
        params['aclass'] = aclass

    if params:
        params = urllib.parse.urlencode(params)
        return r.get(KRAKEN_BASE_URL + api_endpoint + params)
    return r.get(KRAKEN_BASE_URL + api_endpoint)

def get_tradable_asset_pairs( pair: Union[str, None] = None, info: str = 'info'):
    api_endpoint = "/0/public/AssetPairs?"
    params = {}
    if pair is not None:
        params['pair'] = pair
    params['info'] = info
    params = urllib.parse.urlencode(params)
    return r.get(KRAKEN_BASE_URL + api_endpoint + params)

def get_ticker_info( pair: str):
    api_endpoint = f"/0/public/Ticker?pair={pair}"
    return r.get(KRAKEN_BASE_URL + api_endpoint)

def get_ohlc( pair: str, interval: int = 1, since: Union[int, None] = None):
    api_endpoint = "/0/public/OHLC?"
    params = {
        'pair': pair,
        'interval': interval
    }
    if since is not None:
        params['since'] = since
    params = urllib.parse.urlencode(params)
    return r.get(KRAKEN_BASE_URL + api_endpoint + params)

def get_order_book( pair: str, count: Union[int, None] = None):
    api_endpoint = "/0/public/Depth?"
    params = {"pair": pair}
    if count is not None:
        params['count'] = count
    params = urllib.parse.urlencode(params)
    return r.get(KRAKEN_BASE_URL + api_endpoint + params)

def get_recent_trades( pair: str, since: Union[str, None] = None):
    api_endpoint = "/0/public/Trades?"
    params = {"pair": pair}
    if since is not None:
        params['since'] = since
    params = urllib.parse.urlencode(params)
    return r.get(KRAKEN_BASE_URL + api_endpoint + params)

def get_recent_spreads( pair: str, since: Union[int, None] = None):
    api_endpoint = "/0/public/Spread?"
    params = {"pair": pair}
    if since is not None:
        params['since'] = since
    params = urllib.parse.urlencode(params)
    return r.get(KRAKEN_BASE_URL + api_endpoint + params)

