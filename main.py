# coding:utf-8
import requests
from bs4 import BeautifulSoup
from http import cookiejar
import time
import iMessage
import datetime
import random
import esprima
import re


class PCPost:
    def __init__(self):
        self.cookies = {}
        # mock the build-in browser of WeChat:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; PCT-AL10 Build/HUAWEIPCT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2575 MMWEBSDK/200701 Mobile Safari/537.36 MMWEBID/4039 MicroMessenger/7.0.17.1720(0x27001137) Process/tools WeChat/arm64 NetType/WIFI Language/en ABI/arm64',
            'Referer': 'https://stu.cugb.edu.cn/webApp/xuegong/index.html',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        self.session = requests.session()
        self.message1 = ''
        self.message2 = ''
        self.message3 = ''
        self.subj = ''
        self.content = ''

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
            # ★Modification needed
            uname = ''  # Input your Student Number, e.g. 2005190001
            upwd = ''  # Input your portals' password, e.g. 123456
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
        if D < 10:
            date = str(Y) + "-" + str(M) + "-" + "0" + str(D)
        else:
            date = str(Y) + "-" + str(M) + "-" + str(D)
        reas_addr = {"买日用品": "民族园路2号",
                     "买水果": "学清路27号",
                     "牙医预约": "花园北路49号",
                     "出去吃饭": "中关村北大街127号",
                     "健身锻炼": "中关村东路16号",
                     "买衣服": "三里屯路19号",
                     "购物": "成府路28号",
                     "购买东西": "中关村西区善缘街1号",
                     "雅思培训": "中关村大街19号",
                     "户外锻炼": "科荟路33号",
                     "呼吸新鲜空气": "科荟路33号",
                     "户外运动": "科荟路33号",
                     "修发理发": "学清路甲8号"}
        reas, addr = random.choice(list(reas_addr.items()))
        return (reas, date, addr)

    def out_apply(self):
        # cookie_para = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
        (reas, date, addr) = self.random_reason()
        # ★Modification needed
        # "c1":"182XXXX1234"---Your telephone number
        # "c7":"学19楼"     ---Your building number
        # "c18":"110X"      ---Your room number
        # 'uploadFileStr': '''{"c16":[]}'''   ---need to be captured from Fiddler or Charles
        datastr = '''{"xmqkb":{"id":"4a4ce9d674438da101745ca20e2b3a5e"},"location_address":"北京市海淀区学院路街道中国地质大学(北京)","location_longitude":"116.35207","location_latitude":"39.953298","c1":"182XXXX1234","c2":"临时出校","c17":"学19楼","c18":"110X","c7":\"%s\","c8":\"%s\","c13":\"%s\","c15":"是","type":"YQSJCJ"}'''
        data = {
            'data': datastr % (reas, date, addr),
            'msgUrl': '''syt/zzapply/list.htm?type=YQSJCJ&xmid=4a4ce9d674438da101745ca20e2b3a5e''',
            'uploadFileStr': '''{"c16":[]}''',
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

    def send_to_wechat(self):
        # ★Modification needed
        api = "https://sc.ftqq.com/[].send"  # Apply an wechat-chan api on ftqq.com and fill the expression
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
                    self.subj = '✔已通过'
                    self.content = """
                    【😃早上好，Francis！】
                    ◉出校请注意安全~(￣▽￣)~*
                    ◉抓紧写论文✍⌨
                    ◉做事不要拖✈💪
                    """
                elif status == 'wh':
                    self.subj = '⏰等待中...'
                    self.content = """
                    【⏰每2分钟查询，请等待...】
                    ◉当前状态：%s
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
    iMessage.send_Message(News=student.message1 + "\n" + "Out-Apply: " + student.message3,
                          sub="Application: " + student.message2)
    student.send_to_wechat()
    while True:  # while True loop
        time.sleep(120)  # wait for 2 minutes
        status = student.check_status()
        if status == 'xz':  # if the status match with the string 'xz', send the status and break the while loop
            student.send_to_wechat()
            break
