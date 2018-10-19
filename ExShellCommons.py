#!/usr/bin/env python
# @Author  : cngeeks
# @Date    : 2018-10-18 18:49:17

import urllib
import urllib.parse
import urllib.request
import base64
import datetime
import requests
import hashlib
import hmac
import json

# 填写您的APIKEY
ACCESS_KEY = ""
SECRET_KEY = ""

API_URL = "https://api.exshell.io"

ACCOUNT_ID = 0

proxies = {}

def send_get_request(_url, _params):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    try:
        with requests.get(_url, _params, headers=headers, timeout=30, proxies=proxies) as response:
            if response.text == "":
                print("ERROR: No data")
                return
            elif response.status_code != 200:
                print("ERROR: status_code = " + str(response.status_code))
                print(response.text)
                return
    except BaseException as e:
        print("HTTP GET FAIL - error msg is %s, %s" %(response.text, e))
        return
    return response.json()


def send_post_request(_url, _params):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    payload = json.dumps(_params)
    try:
        with requests.post(_url, payload, headers=headers, timeout=30, proxies=proxies) as response:
            if response.text == "":
                print("ERROR: No data")
                return
            elif response.status_code != 200:
                print("ERROR: status_code = " + str(response.status_code))
                print(response.text)
                return
    except BaseException as e:
        print("HTTP POST FAIL - error msg is %s, %s" %(response.text, e))
        return
    return response.json()


def send_auth_get_request(_params, _request_path):
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    _params.update({'AccessKeyId': ACCESS_KEY,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': timestamp})
    host_name = urllib.parse.urlparse(API_URL).hostname.lower()
    _params['Signature'] = create_signature(_params, 'GET', host_name, SECRET_KEY)
    url = API_URL + _request_path
    return send_get_request(url, _params)


def send_auth_post_request(_params, _request_path):
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params_to_sign = {'AccessKeyId': ACCESS_KEY,
                      'SignatureMethod': 'HmacSHA256',
                      'SignatureVersion': '2',
                      'Timestamp': timestamp}
    host_name = urllib.parse.urlparse(API_URL).hostname.lower()
    params_to_sign['Signature'] = create_signature(params_to_sign, 'POST', host_name, SECRET_KEY)
    url = API_URL + _request_path + '?' + urllib.parse.urlencode(params_to_sign)
    return send_post_request(url, _params)


def create_signature(_params, _method, _host, _secret_key):
    sorted_params = sorted(_params.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [_method, _host, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    _secret_key = _secret_key.encode(encoding='UTF8')
    digest = hmac.new(_secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature
