# coding:utf-8
import requests
from bs4 import BeautifulSoup
from http import cookiejar
import time
#import iMessage
import datetime
import random
import esprima
import re
import json


class PCPost:
    def __init__(self):
        self.cookies = {}
        # mock the build-in browser of WeChat:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.2(0x18000237) NetType/4G Language/en',
            'Referer': 'https://stu.cugb.edu.cn/webApp/xuegong/index.html',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        self.session = requests.session()
        self.message1 = ''
        self.message2 = ''
        self.message3 = ''
        self.subj = ''
        self.content = ''
        f = open('/usr/local/src/CUGBAutoSubmit/config.json', 'r', encoding='utf-8')
        self.tmp = f.read()
        f.close()
        self.userconfig = json.loads(self.tmp)

    def login(self):
        try:
            # # (Invalid now due to the websites' update)
            # #  Request the cookie and token from the origin web:
            # originurl = 'https://stu.cugb.edu.cn'
            # req = self.session.get(originurl)
            # set_cookie = requests.utils.dict_from_cookiejar(req.cookies)
            # header_cookie = 'JSESSIONID' + '=' + str(set_cookie['JSESSIONID']) + ';' + 'token' + '=' + str(set_cookie['token'])
            # #Add the cookie and token into headers:
            # self.headers['Cookie'] = header_cookie
            # A new feature for the site that uses base64 encoding for the username and password, and uses token:
            # uname_encrypt = str(base64.b64encode(uname.encode('utf-8')), 'utf-8')
            # upwd_encrypt = str(base64.b64encode(upwd.encode('utf-8')), 'utf-8')
            # token = str(set_cookie['token'])
            # data = {'username': uname_encrypt, 'password': upwd_encrypt, 'verification': '', 'token': token}

            # CAS Unified Auth:
            url = 'https://cas.cugb.edu.cn/login'
            req = self.session.request('GET', url, verify=False).content
            soup = BeautifulSoup(req, 'html.parser')
            execution = soup.findAll("input", {"name": "execution"})[0]["value"]
            system = soup.findAll("input", {"id": "userLoginSystem"})[0]["value"]
            uname = self.userconfig['username']
            upwd = self.userconfig['password']
            data = {'username': uname,
                    'password': upwd,
                    'execution': execution,
                    '_eventId': 'submit',
                    'geolocation': '',
                    'loginType': 'username',
                    'system': system,  # '27A5A4DF0C874122A0AFE0367F0A3F46'
                    'enableCaptcha': 'N'}
            req = self.session.post(url=url, data=data, headers=self.headers, verify=False)
            self.cookies = requests.utils.dict_from_cookiejar(req.cookies)
            time.sleep(3)
            # To get the uid from javascript:
            uidurl = 'https://stu.cugb.edu.cn/'
            req = self.session.request('GET', uidurl, cookies=self.cookies, headers=self.headers, verify=False).content
            soup = BeautifulSoup(req, 'html.parser')
            scriptTags = str(soup.findAll('script')[1])
            rexp = re.compile(r'<[^>]+>', re.S)
            scriptCode = rexp.sub('', scriptTags)
            uid = esprima.tokenize(scriptCode)[48].value.replace('\'', '')
            uiddata = {'uid': uid}
            req = self.session.request('POST', "https://stu.cugb.edu.cn:443/caswisedu/login.htm", data=uiddata,
                                       verify=False)
            time.sleep(3)
            content = self.session.post(
                'https://stu.cugb.edu.cn/webApp/xuegong/index.html#/zizhu/apply?projectId=4a4ce9d674438da101745ca20e2b3a5e&type=YQSJCJ', verify=False)
            if content.status_code == 200:
                self.message1 = "Login status: Succeeded"
                time.sleep(3)
                self.out_apply()
            else:
                self.message1 = "Login status: Failed"
        except Exception as e:
            self.message1 = 'Error Code 0: ' + str(e)

    def random_reason(self):
        Y = datetime.datetime.now().year
        M = datetime.datetime.now().month
        D = datetime.datetime.now().day + 1
        date = ''
        if D < 10:
            if M in [10, 11, 12]:
                date = str(Y) + "-" + str(M) + "-" + "0" + str(D)
            else:
                date = str(Y) + "-" + "0" + str(M) + "-" + "0" + str(D)
        elif D <= 32:
            if M == 2:
                if (Y % 4 == 0 and Y % 100 != 0) or Y % 400 == 0:
                    if D == 30:
                        M = M + 1
                        D = 1
                        date = str(Y) + "-" + "0" + str(M) + "-" + "0" + str(D)
                    else:
                        date = str(Y) + "-" + "0" + str(M) + "-" + str(D)
                else:
                    if D == 29:
                        M = M + 1
                        D = 1
                        date = str(Y) + "-" + "0" + str(M) + "-" + "0" + str(D)
                    else:
                        date = str(Y) + "-" + "0" + str(M) + "-" + str(D)
            elif M in [1, 3, 5, 7, 8]:
                if D == 32:
                    M = M + 1
                    D = 1
                    date = str(Y) + "-" + "0" + str(M) + "-" + "0" + str(D)
                else:
                    date = str(Y) + "-" + "0" + str(M) + "-" + str(D)
            elif M == 10:
                if D == 32:
                    M = M + 1
                    D = 1
                    date = str(Y) + "-" + str(M) + "-" + "0" + str(D)
                else:
                    date = str(Y) + "-" + str(M) + "-" + str(D)
            elif M == 12:
                if D == 32:
                    Y = Y + 1
                    M = 1
                    D = 1
                    date = str(Y) + "-" + "0" + str(M) + "-" + "0" + str(D)
                else:
                    date = str(Y) + "-" + str(M) + "-" + str(D)
            elif M in [4, 6]:
                if D == 31:
                    M = M + 1
                    D = 1
                    date = str(Y) + "-" + "0" + str(M) + "-" + "0" + str(D)
                else:
                    date = str(Y) + "-" + "0" + str(M) + "-" + str(D)
            elif M == 9:
                if D == 31:
                    M = M + 1
                    D = 1
                    date = str(Y) + "-" + str(M) + "-" + "0" + str(D)
                else:
                    date = str(Y) + "-" + "0" + str(M) + "-" + str(D)
            elif M == 11:
                if D == 31:
                    M = M + 1
                    D = 1
                    date = str(Y) + "-" + str(M) + "-" + "0" + str(D)
                else:
                    date = str(Y) + "-" + str(M) + "-" + str(D)
        reas_addr = self.userconfig["reas_addr"]
        reas, addr = random.choice(list(reas_addr.items()))
        return (reas, date, addr)

    def out_apply(self):
        # cookie_para = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
        (reas, date, addr) = self.random_reason()
        datastr = '''{"xmqkb":{"id":"4a4ce9d674438da101745ca20e2b3a5e"},"c2":"临时出校","c7":\"%s\","c13":\"%s\","c3":\"%s\","c8":\"%s\","type":"YQSJCJ","location_longitude":"116.359231","location_latitude":"39.893642","location_address":"北京市海淀区学院路街道中国地质大学(北京)"}'''
        data = {
            'data': datastr % (reas, addr, "公交", date),
            'msgUrl': '''syt/zzapply/list.htm?type=YQSJCJ&xmid=4a4ce9d674438da101745ca20e2b3a5e''',
            'uploadFileStr': str(self.userconfig['upfile']),
            'multiSelectData': '''{}'''}
        while True:
            try:
                r = self.session.request('POST', url='https://stu.cugb.edu.cn:443/syt/zzapply/operation.htm',
                                         headers=self.headers, cookies=self.cookies, data=data, verify=False)
                print(r.status_code)
                if r.text == 'success':
                    self.message2 = 'Succeeded'
                    self.message3 = reas + "\n" + date + "\n" + addr
                    self.subj = '☛已提交，等待系统自动通过...'
                    self.content = """
                    【提交信息☟】
                    日期：%s
                    事由：%s
                    地址：%s
                    """ % (date, reas, addr)
                elif r.text == 'Applied today':
                    self.message2 = 'Applied today'
                    self.message3 = reas + "\n" + date + "\n" + addr
                    self.subj = '☛今日已提交！'
                    self.content = """
                    【提交信息☟】
                    日期：%s
                    事由：%s
                    地址：%s
                    """ % (date, reas, addr)
                else:
                    self.message2 = 'Failed. Please check it'
                    self.message3 = reas + "\n" + date + "\n" + addr
                    self.subj = '☛出现异常，请查看日志！'
                    self.content = """
                    【提交信息☟】
                    日期：%s
                    事由：%s
                    地址：%s
                    """ % (date, reas, addr)
            except Exception as e:
                self.message2 = 'Error Code 1: ' + str(e)
                self.message3 = reas + "\n" + date + "\n" + addr
                self.subj = '☛出现异常，请查看日志！'
                self.content = """
                【⚠警告！抛出异常代码！⚠】
                %s
                【提交信息☟】
                日期：%s
                事由：%s
                地址：%s
                """ % (self.message2, date, reas, addr)
                time.sleep(3)
            else:
                break

    def send_to_phone(self):
        api = self.userconfig["push_api"]
        data = {
            "text": self.subj,
            "desp": self.content}
        requests.post(api, data=data, verify=False)

    def check_status(self):
        while True:
            try:
                data = {'pageIndex': '0', 'pageSize': '10', 'xmid': '4a4ce9d674438da101745ca20e2b3a5e',
                        'type': 'YQSJCJ'}
                r = self.session.request('POST', url='https://stu.cugb.edu.cn/syt/zzapply/queryxssqlist.htm',
                                         headers=self.headers, cookies=self.cookies, data=data, verify=False)
                applyid = re.findall(re.compile(r'\"id\":\"(.*?)\"'), r.text)[0]
                data = {'id': applyid}
                r = self.session.request('POST',
                                         url='https://stu.cugb.edu.cn:443/syt/zzapi/getApproveStatusByApplyId.htm',
                                         headers=self.headers, cookies=self.cookies, data=data, verify=False)
                status = re.findall(re.compile(r'\"data\":\"(.*?)\"'), r.text)[0]
                if status == 'xz':
                    self.subj = '√Approved'
                    self.content = """
                    【😃Morning！】
                    ◉Protect yourself when going outside.~(￣▽￣)~*
                    ◉Actions speak louder than words.✍⌨
                    ◉Do not go gentle into that good night.💪
                    """
                elif status == 'wh':
                    self.subj = '⏰Waiting...'
                    self.content = """
                    【⏰Waiting for another 2 minutes...】
                    ◉Status：%s
                    """ % r.text
                else:
                    self.subj = '☛出现异常，请查看日志！'
                    self.content = """
                    【⚠出现异常，请查看日志！】
                    """
            except Exception as e:
                self.message1 = 'Error Code 2: ' + str(e)
                print(self.message1)
                time.sleep(600)  # if exceptions happened, wait for 5 minutes
            else:
                break  # if no exceptions happened, break the while loop
        return status


if __name__ == '__main__':
    student = PCPost()
    student.login()
    #iMessage.send_Message(News=student.message1 + "\n" + "Out-Apply: " + student.message3,
    #                      sub="Application: " + student.message2)
    student.send_to_phone()
    # time.sleep(120)  # wait for 2 minutes to check status
    # status = student.check_status()
    # while status != 'xz':  # once status doesn't match with "xz", into while loop
    #     time.sleep(120)
    #     status = student.check_status()  # wait for 2 minutes
    #     student.send_to_wechat()  # send status
    #
    while True:  # while True loop
        time.sleep(120)  # wait for 2 minutes
        status = student.check_status()
        if status == 'xz':  # if the status match with the string 'xz', send the status and break the while loop
            student.send_to_phone()
            break
