from typing import Union

import requests as r

from .utils import _create_data, _send_req


def get_account_balance() -> r.Response:
    api_endpoint = "/0/private/Balance"
    data = _create_data()
    print(data)
    return _send_req(api_endpoint, data)


def get_trade_balance(asset: str) -> r.Response:
    api_endpoint = "/0/private/TradeBalance"
    data = _create_data(asset=asset)
    return _send_req(api_endpoint, data)


def get_open_orders(trades: bool = False, userref: Union[int, None] = None) -> r.Response:
    api_endpoint = "/0/private/OpenOrders"
    data = _create_data(trades=trades, userref=userref)
    return _send_req(api_endpoint, data)


def get_closed_orders(trades: bool = False, userref: Union[int, None] = None, start: int = None, end: int = None, ofs: int = None, closetime: str = "both"):
    api_endpoint = "/0/private/ClosedOrders"
    data = _create_data(
        trades=trades, userref=userref, start=start, end=end, ofs=ofs, closetime=closetime)
    return _send_req(api_endpoint, data)


def query_orders_info(txid: str, trades: bool = False, userref: Union[int, None] = None):
    api_endpoint = "/0/private/QueryOrders"
    data = _create_data(txid=txid, trades=trades, userref=userref)
    return _send_req(api_endpoint, data)


def get_trades_history(type: str = "all", trades: bool = False, start: Union[int, None] = None, end: Union[int, None] = None, ofs: Union[int, None] = None):
    api_endpoint = "/0/private/TradesHistory"
    data = _create_data(
        type=type, trades=trades, start=start, end=end, ofs=ofs)
    return _send_req(api_endpoint, data)


def query_trades_info(txid: str, trades: bool = False):
    api_endpoint = "/0/private/QueryTrades"
    data = _create_data(txid=txid, trades=trades)
    return _send_req(api_endpoint, data)


def get_open_positions(txid: Union[str, None] = None, docalcs: bool = False, consolidation: str = 'market'):
    api_endpoint = "/0/private/OpenPositions"
    data = _create_data(
        txid=txid, docalcs=docalcs, consolidation=consolidation)
    return _send_req(api_endpoint, data)


def get_ledgers_info(asset: str = 'all', aclass: str = 'currency', type: str = 'all', start: Union[int, None] = None, end: Union[int, None] = None, ofs: Union[int, None] = None):
    api_endpoint = "/0/private/Ledgers"
    data = _create_data(
        asset=asset, aclass=aclass, type=type, start=start, end=end, ofs=ofs)
    return _send_req(api_endpoint, data)


def query_ledgers(id: Union[str, None] = None, trades: bool = False):
    api_endpoint = "/0/private/QueryLedgers"
    data = _create_data(id=id, trades=trades)
    return _send_req(api_endpoint, data)


def get_trade_volume(pair: str, fee_info: bool = False):
    api_endpoint = "/0/private/TradeVolume"
    data = _create_data(pair=pair, fee_info=fee_info)
    return _send_req(api_endpoint, data)


def request_export_report(report: str, description: str, format: str = 'csv', fields: str = 'all', starttm: Union[int, None] = None, endtm: Union[int, None] = None):
    api_endpoint = "/0/private/AddExport"
    data = _create_data(report=report, description=description,
                        format=format, fields=fields, starttm=starttm, endtm=endtm)
    return _send_req(api_endpoint, data)


def get_export_reqort_status(report: str):
    api_endpoint = "/0/private/ExportStatus"
    data = _create_data(report=report)
    return _send_req(api_endpoint, data)


def retrieve_data_export(id: str):
    api_endpoint = "/0/private/RetrieveExport"
    data = _create_data(id=id)
    return _send_req(api_endpoint, data)


def delete_export_report(id: str, type: str):
    api_endpoint = "/0/private/RemoveExport"
    data = _create_data(id=id, type=type)
    return _send_req(api_endpoint, data)
