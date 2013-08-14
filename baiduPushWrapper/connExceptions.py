#coding=utf8
__author__ = 'Alexander.Li'

class AccessError(SystemError):
    """
    错误类，用于区分其他底层异常
    """
    def __init__(self, *argv, **kwargs):
        super(AccessError).__init__(*argv, **kwargs)
