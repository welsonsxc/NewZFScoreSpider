# -*- coding: utf-8 -*-
import binascii
import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import rsa


class Student:
    sessions = requests.Session()
    time = int(time.time())

    def __init__(self, name, password, login_url, key_url, grade_url):
        self.pub = None
        self.request = None
        self.year = None
        self.term = None
        self.token = None
        self.header = None
        self.cookie = None
        self.modules = None

        self.name = str(name).encode("utf8").decode("utf8")
        self.password = str(password).encode("utf8").decode("utf8")
        self.url = login_url
        self.KeyUrl = key_url
        self.gradeUrl = grade_url
        self.get_public_key()
        self.get_csrf_token()
        self.process_public()
        self.login()

    # 获取公钥密码
    def get_public_key(self):
        result = self.sessions.get(self.KeyUrl + str(self.time)).json()
        self.modules = result["modulus"]
        # 说实话 这也太那啥了 这居然是没用的 怪不得去年栽在这里
        # self.exponent = result["exponent"]

    # 获取CsrfToken
    def get_csrf_token(self):
        r = self.sessions.get(self.url + str(self.time))
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        self.token = soup.find('input', attrs={'id': 'csrftoken'}).attrs['value']

    # 加密密码
    def process_public(self):
        weibo_rsa_e = 65537
        message = str(self.password).encode()
        rsa_n = binascii.b2a_hex(binascii.a2b_base64(self.modules))
        key = rsa.PublicKey(int(rsa_n, 16), weibo_rsa_e)
        encropy_pwd = rsa.encrypt(message, key)
        self.password = binascii.b2a_base64(encropy_pwd)

    def login(self):
        try:
            self.header = {
                'Accept': 'text/html, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Connection': 'keep-alive',
                'Referer': self.url + str(self.time),
                'Upgrade-Insecure-Requests': '1',
            }
            data = {
                'csrftoken': self.token,
                'mm': self.password,
                'mm': self.password,
                'yhm': self.name
            }
            self.request = self.sessions.post(self.url, headers=self.header, data=data)
            self.cookie = self.request.request.headers['cookie']
            key_word = r'用户名或密码不正确'
            if re.findall(key_word, self.request.text):
                print('用户名或密码错误,请查验..')
                sys.exit()
            else:
                print("登陆成功")
        except Exception as e:
            print(str(e))
            sys.exit()

    def post_grade_data(self):
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
            self.request = self.sessions.post(self.gradeUrl, data=data, headers=self.header).json()
        except Exception as e:
            print(str(e))
            sys.exit()

    def welcome(self):
        try:
            # 姓名
            name = self.request['items'][0]['xm']
            # 学历
            sch_stu = self.request['items'][0]['xslb']
            # 学院
            institute = self.request['items'][0]['jgmc']
            # 班级
            stu_class = self.request['items'][0]['bj']
            print('姓名:{}\t学历:{}\t\t学院:{}\t班级:{}'.format(name, sch_stu, institute, stu_class))
        except Exception as e:
            print(str(e))

    def print_grades(self):
        try:
            plt = '{0:<20}{1:<5}{2:<5}{3:<5}'
            print(plt.format('课程', '成绩', '绩点', '教师'))
            for i in self.request['items']:
                print(plt.format(i['kcmc'], i['bfzcj'], i['jd'], i['jsxm']))
        except Exception as e:
            print("[Error]" + str(e))


if __name__ == '__main__':
    # 输入学号密码
    # stu_name = input('请输入学号:').strip()
    stu_name = "你的学号"
    # stu_password = getpass.getpass('请输入密码(密码不回显,输入完回车即可):') .strip()
    stu_password = "你的密码"

    # 教务系统登录路径
    url = "http://你的学校域名或者ip地址/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t="
    # 请求PublicKey的URL
    key_url = "http://你的学校域名或者ip地址/jwglxt/xtgl/login_getPublicKey.html?time="
    # 获取成绩路径
    grade_url = "http://你的学校域名或者ip地址/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005"

    # 登陆~
    temp = Student(stu_name, stu_password, url, key_url, grade_url)
    # 设定学年
    temp.year = "2018"
    # 第一学期为3 第二学期为12
    temp.term = "3"
    # 选择成绩查询
    temp.post_grade_data()
    # 输出个人信息
    temp.welcome()
    # 输出成绩信息
    temp.print_grades()
