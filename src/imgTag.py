# author ：fengbiao
from src import config
import datetime
import base64
import hmac
import hashlib
from urllib.parse import urlparse
import requests
import json

class HttpClient(object):
    @staticmethod
    def get(self, url, param):
        current_time = self.get_current_date()
        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
            "date": current_time,
        }
        request_body = json.dumps(param)
        request_header.setdefault('authorization', self.get_authorization(current_time, self.set_request_body(request_body)))
        responses = requests.post(url=url, data=request_body, headers=request_header)
        return responses.text

    def post(self, url, param):
        current_time = self.get_current_date()
        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
            "date": current_time,
        }
        request_body = json.dumps(param)
        request_header.setdefault('authorization',
                                  self.get_authorization(url, current_time, self.set_request_body(request_body)))
        responses = requests.post(url=url, data=request_body, headers=request_header)
        return responses.text

    def get_authorization(self, url, current_time, request_body):
        urlPath = urlparse(url)
        if urlPath.query != '':
            urlPath = urlPath.path + "?" + urlPath.query
        else:
            urlPath = urlPath.path
        stringToSign = "POST" + '\n' + "application/json" + '\n' + str(
            request_body) + '\n' + "application/json" + '\n' + current_time + '\n' + str(urlPath)
        signature = self.to_sha1_base64(stringToSign, config.APPSECRT)
        authHeader = 'Dataplus ' + str(config.APPID) + ':' + str(signature)
        return authHeader

    def get_current_date(self):
        date = datetime.datetime.strftime(datetime.datetime.utcnow(), "%a, %d %b %Y %H:%M:%S GMT")
        return date

    def to_sha1_base64(self, string_to_sign, secret):
        hmacsha1 = hmac.new(secret.encode(), string_to_sign.encode(), hashlib.sha1)
        return base64.b64encode(hmacsha1.digest()).decode('utf-8')

    #  设置请求 body
    def set_request_body(self, body):
        hash = hashlib.md5()
        hash.update(body.encode())
        return base64.b64encode(hash.digest()).decode('utf-8')
