# cert_manage
证书管理系统

![Total visitor](https://visitor-count-badge.herokuapp.com/total.svg?repo_id=cert_manage)
![Visitors in today](https://visitor-count-badge.herokuapp.com/today.svg?repo_id=cert_manage)
[![Python3](https://img.shields.io/badge/python-3.6-green.svg?style=plastic)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-2.1.11-brightgreen.svg?style=plastic)](https://www.djangoproject.com/)

---

Cert_manage 是一个开源的证书管理系统，用于检测证书到期日期并提醒管理者，支持基于URL的在线检测和PEM文件离线检测，支持WEB SSL证书、APP开发者证书、APP推送证书等，使用MIT开源协议

Cert_manage 使用 Python / Django 进行开发，遵循 Web 2.0 规范

![主页面](https://www.itnotebooks.com/wp-content/uploads/2019/09/主页面截图-1.png)


# 安装文档

## 安装Python 3.6

~~~
参考网上其它文档
~~~

## 创建虚拟环境

~~~
$ python3 -m venv /opt/py3
~~~

## 载入虚拟环境

~~~
$ source /opt/py3/bin/activate
~~~

## 获取cert_mange代码

~~~
$ cd /opt/
$ git clone --depth=1 https://github.com/itnotebooks/cert_manage.git
# 如果没有安装 git 请先安装
~~~

## 安装依赖

~~~
$ cd /opt/cert_manage
$ pip install -r requirements/requirements.txt
~~~

## 修改配置文件

~~~
$ cd /opt/cert_manage
$ cp config_example.py config.py
$ vim config.py
~~~

## 启动 cert_manage

~~~
$ cd /opt/cert_manage
$ python run_server.py
~~~

## 访问

~~~
http://127.0.0.1:8080
初始用户名：admin
初始密码：admin
~~~
