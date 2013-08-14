#coding=utf8
__author__ = 'Alexander.Li'

class AccessError(Exception):
    """
    错误类，用于区分其他底层异常
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

