#!/usr/bin/env python
# @Author  : cngeeks
# @Date    : 2018-10-18 18:49:17

from ExShellCommons import *

"""
获取K线
参数：
_symbol: 交易对
_period: 时间区间，可选值：1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
_size: 数量，可选区间 1 至 2000
"""
def get_kline(_symbol, _period, _size=150):
    params = {'symbol': _symbol,
              'period': _period,
              'size': _size}
    url = API_URL + '/v1/mkt/kline'
    return send_get_request(url, params)

"""
获取单个交易对聚合行情
参数：
_symbol: 交易对
"""
def get_ticker(_symbol):
    params = {'symbol': _symbol}
    url = API_URL + '/v1/mkt/aggregated'
    return send_get_request(url, params)

"""
获取全部交易对交易行情
参数：
_symbol: 交易对
"""
def get_tickers():
    params = {}
    url = API_URL + '/v1/mkt/tickers'
    return send_get_request(url, params)

"""
获取市场深度
参数：
_symbol: 交易对
_type: 类型，可选值：percent10, step0, step1, step2, step3, step4, step5
"""
def get_depth(_symbol, _type):
    params = {'symbol': _symbol,
              'type': _type}
    url = API_URL + '/v1/mkt/depth'
    return send_get_request(url, params)

"""
获取单个交易对最新一笔成交记录
参数：
_symbol: 交易对
"""
def get_trade(_symbol):
    params = {'symbol': _symbol}
    url = API_URL + '/v1/mkt/trade'
    return send_get_request(url, params)

"""
获取单个交易对历史成交记录
参数：
_symbol: 交易对
_size: 获取的记录数量，取值区间 1 至 2000
"""
def get_tradeHistory(_symbol, _size=5):
    params = {'symbol': _symbol,
              'size': _size}
    url = API_URL + '/v1/mkt/tradeHistory'
    return send_get_request(url, params)

"""
获取单个交易对24小时交易聚合行情
参数：
_symbol: 交易对
"""
def get_last24hr(_symbol):
    params = {'symbol': _symbol}
    url = API_URL + '/v1/mkt/last24hr'
    return send_get_request(url, params)

"""
获取支持的所有交易对和报价精度
"""
def get_symbols():
    params = {}
    url = API_URL + '/v1/pub/symbols'
    return send_get_request(url, params)

"""
获取支持的所有交易币种
"""
def get_currencies():
    params = {}
    url = API_URL + '/v1/pub/currencies'
    return send_get_request(url, params)

"""
获取系统时间
"""
def get_timestamp():
    params = {}
    url = API_URL + '/v1/pub/timestamp'
    return send_get_request(url, params)

"""
查询当前用户的所有账户状态
"""
def get_accounts():
    path = "/v1/priv/accounts"
    params = {}
    return send_auth_get_request(params, path)

"""
查询账户ID
"""
def get_account_id():
    account_id = None
    try:
        accounts = get_accounts()
        account_id = accounts['data'][0]['id']
    except BaseException as e:
        print ('ERROR: %s' % e)
    return account_id

"""
查询单个账户资产
"""
def get_balance(_account_id=None):
    if not _account_id:
        acc_id = get_account_id()
    url = "/v1/priv/accounts/{0}/balance".format(acc_id)
    params = {"account-id": acc_id}
    return send_auth_get_request(params, url)


"""
交易下单
参数：
_amount: 下单数量
_source: api
_symbol: 交易对
_type: 下单类型，可选值：buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖
_price: 下单价格
"""
def place_order(_amount, _source, _symbol, _type, _price=0):
    acct_id = get_account_id()
    params = {"account-id": acct_id,
              "amount": _amount,
              "symbol": _symbol,
              "type": _type,
              "source": _source}
    
    if _price:
        params["price"] = _price
    url = '/v1/priv/orders/place'
    return send_auth_post_request(params, url)

"""
撤销单个订单
参数：
_order_id: 订单ID
"""
def cancel_order(_order_id):
    params = {}
    url = "/v1/priv/orders/{0}/cancel".format(_order_id)
    return send_auth_post_request(params, url)

"""
批量撤销未成交订单
参数：
_symbol: 交易对
_side: 可选值: buy，sell
_size: 数量，取值区间 1 至 500，默认值 10
"""
def batch_cancel_open_orders(_account_id, _symbol, _side=None, _size=None):
    params = {"account-id": _account_id
             , "symbol": _symbol}
    if _side:
        params["side"] = _side
    if _size:
        params["size"] = _size
    url = "/v1/priv/orders/batchCancelEx"
    return send_auth_post_request(params, url)

"""
根据订单ID查询订单详情
参数：
_order_id: 订单ID
"""
def order_info(_order_id):
    params = {}
    url = "/v1/priv/orders/{0}".format(_order_id)
    return send_auth_get_request(params, url)

"""
根据订单ID查询订单的成交明细
参数：
_order_id: 订单ID
"""
def order_matchresults(_order_id):
    params = {}
    url = "/v1/priv/orders/{0}/matchResults".format(_order_id)
    return send_auth_get_request(params, url)

"""
查询当前委托单、历史委托单
参数：
_symbol: 交易对
_state: 状态，可选值: pre-submitted 准备提交, submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销
_type: 下单类型，可选值：buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖
_direct: 可选值: prev 向前，next 向后
_size: 数量，取值区间 1 至 100
"""
def orders_list(_symbol, _states, _types=None, _start_date=None, _end_date=None, _from=None, _direct=None, _size=None):
    params = {'symbol': _symbol,
              'states': _states}
    if _types:
        params['types'] = _types
    if _start_date:
        params['start-date'] = _start_date
    if _end_date:
        params['end-date'] = _end_date
    if _from:
        params['from'] = _from
    if _direct:
        params['direct'] = _direct
    if _size:
        params['size'] = _size
    url = '/v1/priv/orders'
    return send_auth_get_request(params, url)

"""
查询当前成交、历史成交
参数：
_symbol: 交易对
_type: 下单类型，可选值：buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖
_direct: 可选值: prev 向前，next 向后
"""
def orders_matchresults(_symbol, _types=None, _start_date=None, _end_date=None, _from=None, _direct=None, _size=None):
    params = {'symbol': _symbol}
    if _types:
        params['types'] = _types
    if _start_date:
        params['start-date'] = _start_date
    if _end_date:
        params['end-date'] = _end_date
    if _from:
        params['from'] = _from
    if _direct:
        params['direct'] = _direct
    if _size:
        params['size'] = _size
    url = '/v1/priv/matchResults'
    return send_auth_get_request(params, url)

"""
查询未成交订单
参数：
_symbol: 交易对
_side: 可选值: buy，sell
_size: 数量，取值区间 1 至 500，默认值 10
"""
def query_open_orders(_account_id, _symbol, _side=None, _size=None):
    params = {"account-id": _account_id
             , "symbol": _symbol}
    if _side:
        params["side"] = _side
    if _size:
        params["size"] = _size
    url = "/v1/priv/order/openOrders"
    return send_auth_get_request(params, url)

