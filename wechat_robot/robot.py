# -*- coding:utf-8 -*-
import werobot
from wechat_robot import dy, sql

robot = werobot.WeRoBot(token='robot')
client = robot.client

robot.config["APP_ID"] = ""
robot.config["APP_SECRET"] = ""
state = 'null'
xh = 'null'
pw = 'null'


@robot.subscribe
def subscribe(message):
    """
    :param message: 关注提示
    :return: str类型 关注提示
    """
    return '感谢关注!'


@robot.key_click("login")
def login(message):
    """
    :param message: 绑定教务按钮
    :return: Bool类型 账号密码正确返回True 失败返回False
    """
    global state
    state = 'input_xh'
    return '请输入学号'


# @robot.key_click("search")
# def search(message):
# openid = message.source
# 呀 这个函数丢失了 我也不知道去哪里了～
# message1 = dy.search1(openid)
# return message1


@robot.filter("test")
def login(message):
    """
    :param message: 发送"test"进行测试 根据openid查找学号密码
    :return: 查询到 return学号密码 如果没有 return绑定网页
    """
    openid = message.source
    fh = r"'"
    openid = fh + openid + fh
    res = sql.sql_openid(openid)
    if res != "":
        reply = "学号:" + res[0][1] + "密码:" + res[0][2]
        return reply
    else:
        reply = "sorry~I can't find you!"
        return reply


@robot.text
def echo(message):
    global state
    global xh
    global pw
    openid = message.source
    if state == "input_xh":
        xh = message.content
        state = 'input_pw'
        return '请输入密码'
    if state == "input_pw":
        pw = message.content
        message1 = sql.insert_pw(openid, xh, pw)
        # message1 = dy.login1(xh, pw, openid)
        return message1


# 自定义菜单
client.create_menu({
    "button": [
        {
            "name": "教务",
            "sub_button": [
                {
                    "type": "click",
                    "name": "学号绑定",
                    "key": "login"
                },
                {
                    "type": "click",
                    "name": "成绩查询",
                    "key": "search"
                }
            ]
        }
    ]
})

# 让服务器监听在 0.0.0.0:80
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
