#coding=utf8
__author__ = 'Alexander.Li'

import requests
import urllib
import hashlib
import time
import json
from connExceptions import AccessError

POST = "POST"
GET = "GET"
CHANNEL = "channel"

class Connection(object):
    """
    主类，用来包含所有的操作和基础参数，用户实例化这个类，传入必要的参数，访问push接口
    参数：
        secury_key： app的ID
        secury_secret： app加密密钥
        use_ssl： 是否使用https来访问接口
        timeout：访问接口超时时间
    示例：c = Connection("xxxxxxxxxxxx","xxxxxxxxxxxxxxx")
    """
    def __init__(self, secury_key, secury_secret, use_ssl=False, timeout=20):
        self.sk = secury_key
        self.ss = secury_secret
        self.base_url = "https://channel.api.duapp.com/rest/2.0/channel/" if use_ssl else "http://channel.api.duapp.com/rest/2.0/channel/"
        self.timeout = timeout

    def _prepare_and_sign(self,method, url, params, **option_params):
        """
        填入必填系统级别参数和将可选参数，生成验证串并放入参数中，返回完整的参数列表
        """
        from operator import itemgetter
        params["apikey"] = self.sk
        params["timestamp"] = int(time.time())
        for k, v in option_params.iteritems():
            if v:
                params[k] = v
        params["expires"] = 600
        param_str = "".join(["=".join([k,str(v)]) for k, v in  sorted(params.iteritems(), key=itemgetter(0), reverse=False)])
        sign_str = "".join([method,url,param_str,self.ss])
        sign_base = urllib.urlencode(dict(p=sign_str))[2:]
        sign = hashlib.md5(sign_base)
        params["sign"] = sign.hexdigest()
        return params

    def _proccess_response(self, response):
        """
        统一处理返回值，如果是200就返回json对象，如果报错就抛出异常，并且将返回对象作为异常的参数
        """
        result = json.loads(response.text)
        if response.status_code ==  200:
            return result
        raise AccessError(result)

    def query_bindlist(self, user_id, channel_id=None, device_type=None, start=0, limit=10):
        """
        获取绑定列表
        参数：
            user_id：用户ID
        可选参数：
            channel_id：频道编号
            device_type：过滤设备类型
            start：开始序号
            limit：取多少条
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url,channel_id if channel_id else CHANNEL, ])
        params = self._prepare_and_sign(
            GET,
            url,
            dict(method = "query_bindlist", user_id = user_id),
            **dict(device_type=device_type, start=start, limit=limit,)
        )
        return self._proccess_response(requests.get(url, params=params, timeout=self.timeout))


    def push_msg(self, user_id, channel_id, push_type, msg_keys, messages, device_type=None, message_type=0,
                 message_expires=None, deploy_status=None):
        """
        推送消息
        参数
            user_id：用户编号
            channel_id：频道编号
            push_type：推送类型 1:单人 2:指定tag 3:所有人
            msg_keys：消息标识
            messages：消息体
        可选参数
            device_type：过滤设备类型
            message_expires：消息过期时间
            deploy_status：IOS专用，是测试环境还是正式环境
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url,"channel"])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="push_msg", push_type=push_type, channel_id=channel_id, msg_keys=msg_keys, messages=messages),
            device_type = device_type,
            message_type = message_type,
            message_expires = message_expires,
            deploy_status = deploy_status,
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def init_app_ioscert(self, channel_id, name, description, release_cert, dev_cert):
        """
        设置IOS的证书
        参数：
            channel_id：频道编号
            name：证书名
            description：证书描述
            release_cert：正式证书
            dev_cert：测试证书
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, channel_id])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="init_app_ioscert", name=name, description=description, release_cert=release_cert, dev_cert=dev_cert)
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def update_app_ioscert(self, channel_id, name, description, release_cert, dev_cert):
        """
        更新IOS的证书
        参数：
            channel_id：频道编号
            name：证书名
            description：证书描述
            release_cert：正式证书
            dev_cert：测试证书
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, channel_id])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="update_app_ioscert", name=name, description=description, release_cert=release_cert, dev_cert=dev_cert)
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def delete_app_ioscert(self, channel_id):
        """
        删除IOS的证书
        参数：
            channel_id：频道编号
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, channel_id])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="delete_app_ioscert")
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def query_app_ioscert(self, channel_id):
        """
        列表所有的IOS证书
        参数：
            channel_id：频道编号
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, channel_id])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="query_app_ioscert")
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def verify_bind(self, channel_id, user_id, device_type=None):
        """
        验证绑定
        参数：
            channel_id：频道编号
            user_id：用户编号
        可选参数：
            device_type：设备类别过滤
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, channel_id])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="verify_bind", user_id=user_id),
            device_type = device_type
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def fetch_msg(self, channel_id, user_id, start=None, limit=None):
        """
        查询消息
        参数：
            channel_id：频道编号
            user_id：用户编号
        可选参数：
            start：开始序号
            limit：一次获取条数
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, channel_id])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="fetch_msg", user_id=user_id),
            start = start,
            limit = limit
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def fetch_msgcount(self, channel_id, user_id):
        """
        查询消息数量
        参数：
            channel_id：频道编号
            user_id：用户编号
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, channel_id])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="fetch_msgcount", user_id=user_id)
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def delete_msg(self, channel_id, user_id, msg_ids):
        """
        删除消息
        参数：
            channel_id：频道编号
            user_id：用户编号
            msg_ids：消息编号列表或者编号，列表就传入一个列表
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, channel_id])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="delete_msg", user_id=user_id, msg_ids=msg_ids)
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def set_tag(self, user_id, tag):
        """
        设置标签
        参数：
            user_id：用户编号
            tag：标签名
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, CHANNEL])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="set_tag", user_id=user_id, tag=tag)
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def fetch_tag(self, user_id, name=None, start=None, limit=None):
        """
        设置标签
        参数：
            user_id：用户编号
        可选参数：
            name：标签名
            start：开始序号
            limit：一次获取条数
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, CHANNEL])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="fetch_tag", user_id=user_id),
            name=name,
            start=start,
            limit=limit
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def delete_tag(self, user_id, tag):
        """
        删除标签
        参数：
            user_id：用户编号
            tag：标签名
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, CHANNEL])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="delete_tag", user_id=user_id, tag=tag)
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def query_user_tags(self, user_id):
        """
        获取用户所有标签
        参数：
            user_id：用户编号
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, CHANNEL])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="query_user_tags", user_id=user_id)
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))

    def query_device_type(self, channel_id):
        """
        设置标签
        参数：
            channel_id：频道编号
        返回：
            失败抛出异常connException.AccessError 成功返回字典,结构见http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api/list#.E6.A6.82.E8.BF.B0
        """
        url = "".join([self.base_url, channel_id])
        params = self._prepare_and_sign(
            POST,
            url,
            dict(method="query_device_type")
        )
        return self._proccess_response(requests.post(url, data=params, timeout=self.timeout))