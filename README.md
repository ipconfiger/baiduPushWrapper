About
---
本python package用于代理百度云推送的Restful API请求，本包的哲学就是一对一翻译，函数名和参数名都和Restful API的定义是一一对应的，关于Restful API的接口参见 [http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api](http://developer.baidu.com/wiki/index.php?title=docs/cplat/push/api)

安装
---
可以通过pip安装

    pip install baiduPushWrapper
    
使用
---
实例化后直接执行和api对应接口名的方法即可

    from baiduPushWrapper import connection
    c = connection.Connection("SK","SS")
    c.push_msg(…)
    
未完待续……
