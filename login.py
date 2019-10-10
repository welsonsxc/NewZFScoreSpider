# -*- coding: utf-8 -*-
import binascii
import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import sys
import rsa


class Student:
    sessions = requests.Session()
    time = int(time.time())

    def __init__(self, user, passwd):
        self.pub = None
        self.req = None
        self.header = None
        self.cookie = None
        self.year = "2018"
        self.term = "3"
        self.modules = None
        self.token = None
        self.user = str(user).encode("utf8").decode("utf8")
        self.passwd = str(passwd).encode("utf8").decode("utf8")
        self.url = 'http://qjxyjw.hznu.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'
        self.get_public()
        self.get_csrftoken()
        self.process_public()
        self.login()
        self.post_gradedata()
        self.welcome()

    # 获取公钥密码
    def get_public(self):
        url = 'http://qjxyjw.hznu.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time=' + str(self.time)
        result = self.sessions.get(url).json()
        self.modules = result["modulus"]
        # 说实话 这也太那啥了 这居然是没用的 怪不得去年栽在这里
        # self.exponent = result["exponent"]

    # 获取CsrfToken
    def get_csrftoken(self):
        url = 'http://qjxyjw.hznu.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t=' + str(self.time)
        r = self.sessions.get(url)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        self.token = soup.find('input', attrs={'id': 'csrftoken'}).attrs['value']

    # 加密密码
    def process_public(self):
        weibo_rsa_e = 65537
        message = str(self.passwd).encode()
        rsa_n = binascii.b2a_hex(binascii.a2b_base64(self.modules))
        key = rsa.PublicKey(int(rsa_n, 16), weibo_rsa_e)
        encropy_pwd = rsa.encrypt(message, key)
        self.passwd = binascii.b2a_base64(encropy_pwd)

    def login(self):
        try:
            url = 'http://qjxyjw.hznu.edu.cn/jwglxt/xtgl/login_slogin.html'
            self.header = {
                'Accept': 'text/html, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
                'Content-Length': '0',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'qjxyjw.hznu.edu.cn',
                'Referer': 'http://qjxyjw.hznu.edu.cn/jwglxt/xtgl/index_initMenu.html?jsdm=&_t=' + str(self.time),
                'Upgrade-Insecure-Requests': '1',
            }
            data = {
                'csrftoken': self.token,
                'mm': self.passwd,
                'mm': self.passwd,
                'yhm': self.user
            }
            self.req = self.sessions.post(url, headers=self.header, data=data)
            self.cookie = self.req.request.headers['cookie']
            ppot = r'用户名或密码不正确'
            if re.findall(ppot, self.req.text):
                print('用户名或密码错误,请查验..')
                sys.exit()
            else:
                print("登陆成功")
        except Exception as e:
            print(str(e))
            sys.exit()

    def post_gradedata(self):
        try:
            data = {'_search': 'false',
                    'nd': int(time.time()),
                    'queryModel.currentPage': '1',
                    'queryModel.showCount': '15',
                    'queryModel.sortName': '',
                    'queryModel.sortOrder': 'asc',
                    'time': '0',
                    'xnm': self.year,
                    'xqm': self.term
                    }
            self.req = self.sessions.post(self.url, data=data, headers=self.header).json()
        except Exception as e:
            print(str(e))
            sys.exit()

    def welcome(self):
        try:
            # 姓名
            stu_name = self.req['items'][0]['xm']
            # 学历
            sch_stu = self.req['items'][0]['xslb']
            # 学院
            institute = self.req['items'][0]['jgmc']
            # 班级
            stu_class = self.req['items'][0]['bj']
            print('')
            print('姓名:{}\t学历:{}\t\t学院:{}\t班级:{}'.format(stu_name, sch_stu, institute, stu_class))
            print('')
            time.sleep(1)
        except Exception as e:
            print(str(e))

    def print_geades(self):
        try:
            plt = '{0:<20}{1:<5}{2:<5}{3:<5}'
            print(plt.format('课程', '成绩', '绩点', '教师'))
            for i in self.req['items']:
                print(plt.format(i['kcmc'], i['bfzcj'], i['jd'], i['jsxm']))
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    # 输入学号密码
    # user = input('请输入学号:').strip()
    user = "2017830402024"
    # passwd = getpass.getpass('请输入密码(密码不回显,输入完回车即可):') .strip()
    passwd = "SCjiaowu287486."
    # 登陆~
    temp = Student(user, passwd)
    temp.print_geades()
