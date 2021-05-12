from .utils import _create_data, _send_req
from typing import Union


def add_order(ordertype: str, type: str, pair: str, **kwargs):
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
    data = _create_data(
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

    return _send_req(api_endpoint, data)


def cancel_order(txid: Union[str, int]):
    api_endpoint = "/0/private/CancelOrder"
    data = _create_data(txid=txid)
    return _send_req(api_endpoint, data)


def cancel_all_orders():
    api_endpoint = "/0/private/CancelAll"
    data = _create_data()
    return _send_req(api_endpoint, data)


def cancel_all_orders_after_x(timeout: int):
    api_endpoint = "/0/private/CancelAllOrdersAfter"
    data = _create_data(timeout=timeout)
    return _send_req(api_endpoint, data)
