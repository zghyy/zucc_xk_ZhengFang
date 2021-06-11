# -*- coding: UTF-8 -*-
import binascii
import os
import sys
import OCR_CODE
from bs4 import BeautifulSoup
import requests
import RW_ACCOUNT
import rsa

# zucc正方教务系统需要用到的一些网站连接以及初始化的抢课数据包
class ZUCC:
    DOMAIN = "xk.zucc.edu.cn"
    MainURL = "http://xk.zucc.edu.cn/default2.aspx"
    InitHeader = {"Host": "xk.zucc.edu.cn", "Connection": "keep-alive",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    CheckCodeURL = "http://xk.zucc.edu.cn"
    CheckCodeHeader = ""
    PlanCourageURL = "http://xk.zucc.edu.cn/xsxk.aspx"
    xsmain = "http://xk.zucc.edu.cn/xs_main.aspx?xh="
    GetCodeKeyURL = "http://xk.zucc.edu.cn/ajaxRequest/Handler1.ashx"


# Account为登录用的账户
class Account:
    def __init__(self, name=None, password=None):
        self.session = requests.Session()
        self.soup = None
        self.POSTDate = {'__LASTFOCUS': "", '__VIEWSTATE': "随机码", '__VIEWSTATEGENERATOR': "9BD98A7D",
                         '__EVENTTARGET': "", '__EVENTARGUMENT': "", 'txtUserName': "", 'TextBox2': "",
                         'txtSecretCode': "-1", 'RadioButtonList1': "学生",
                         'Button1': "登录",'txtKeyExponent': "010001",'txtKeyModulus': "随机码"}
        self.account_data = RW_ACCOUNT.read_account()
        if name == None and password == None:
            self.POSTDate["txtUserName"] = self.account_data["username"]
            self.POSTDate["TextBox2"] = self.account_data["password"]
        else:
            self.POSTDate["txtUserName"] = name
            self.POSTDate["TextBox2"] = password
        self.name = ""

    def __refresh_code(self):
        # 获取验证码
        # self.POSTDate["button2"] = "刷新验证码"
        # res = self.session.post(url=ZUCC.CheckCodeURL, data=self.POSTDate, headers=ZUCC.InitHeader)
        # imgsoup = BeautifulSoup(res.text, 'lxml')
        imgs = self.soup.find_all("img")
        useimg = ""
        for img in imgs:
            if img.get("id") == "icode":
                useimg = img.get("src")
        image_response = self.session.get(ZUCC.CheckCodeURL + useimg, stream=True)

        image = image_response.content
        try:
            with open(os.getcwd() + "/code.gif", "wb") as code_gif:
                img_dir = os.getcwd() + "/"
                code_gif.write(image)
            code_gif.close()
        except IOError:
            print("IO ERROR!")
        finally:
            return img_dir

    def __get_check_code_human(self):
        while self.POSTDate["txtSecretCode"] == "-1":
            img_dir = self.__refresh_code()
            os.startfile(img_dir + "code.gif")
            self.POSTDate["txtSecretCode"] = input("Input checkCode(-1 to refresh):")

    def __get_check_code_ocr(self):
        img_dir = self.__refresh_code()
        print("###Identify checkCode")
        self.POSTDate['txtSecretCode'] = OCR_CODE.run(img_dir, dir_now=img_dir)
        # print(self.POSTDate['txtSecretCode'])

    # 登录进入主页
    def login(self):
        print("#Begin to login")
        # print("##Get init page")
        while True:
            init_response = self.session.get(url=ZUCC.MainURL, headers=ZUCC.InitHeader)
            if init_response.ok:
                print("##GET login page succeed!")
                break
        self.soup = BeautifulSoup(init_response.text, "lxml")
        self.POSTDate["__VIEWSTATE"] = self.soup.find('input', attrs={'name': '__VIEWSTATE'})["value"]
        self.POSTDate["txtKeyModulus"] = self.soup.find('input', attrs={'name': 'txtKeyModulus'})["value"]
        # print("###GET StateCode:", self.POSTDate["__VIEWSTATE"])  # 随机码
        # print("###GET txtKeyModulus:", self.POSTDate["txtKeyModulus"])  # KeyModulus
        # print("###GET checkCode")
        message = self.POSTDate["TextBox2"]
        # print("message":message)
        exponent = int(self.POSTDate["txtKeyExponent"],16)
        modulus = int(self.POSTDate["txtKeyModulus"],16)
        rsa_pubkey = rsa.PublicKey(modulus, exponent)
        # print("rsa_pubkey:"rsa_pubkey)
        passwd = rsa.encrypt(message.encode('utf-8'), rsa_pubkey)
        # print("passwd:"passwd)
        passwd = binascii.b2a_hex(passwd).decode('ascii')
        self.POSTDate["TextBox2"] = passwd

        self.__get_check_code_ocr()
        print("##POST login")
        try_time = 0
        login_response = self.session.post(ZUCC.MainURL, data=self.POSTDate,headers=ZUCC.InitHeader)
        while try_time < 300:
            login_response = self.session.get(ZUCC.xsmain + self.account_data["username"], headers=ZUCC.InitHeader)
            # 进入主页
            self.soup = BeautifulSoup(login_response.text, "lxml")
            if login_response.ok and self.soup.find("title").text == "正方教务管理系统":
                print("#Login：" + self.soup.find("title").text)
                self.name = self.soup.find("span", id="xhxm").text[0:-2]
                print("#姓名：", self.name)
                print("\033[1;36m 登录成功 \033[0m")
                return
            else:
                try_time += 1
        print("#Check account password and restart!")
        sys.exit()


class Encrypt(object):
    def __init__(self, e, m):
        self.e = e
        self.m = m

    def encrypt(self, message):
        mm = int(self.m, 16)
        ee = int(self.e, 16)
        rsa_pubkey = rsa.PublicKey(mm, ee)
        crypto = self._encrypt(message.encode(), rsa_pubkey)
        return crypto.hex()

    def _pad_for_encryption(self, message, target_length):
        message = message[::-1]
        max_msglength = target_length - 11
        msglength = len(message)

        padding = b''
        padding_length = target_length - msglength - 3

        for i in range(padding_length):
            padding += b'\x00'

        return b''.join([b'\x00\x00', padding, b'\x00', message])

    def _encrypt(self, message, pub_key):
        keylength = rsa.common.byte_size(pub_key.n)
        padded = self._pad_for_encryption(message, keylength)

        payload = rsa.transform.bytes2int(padded)
        encrypted = rsa.core.encrypt_int(payload, pub_key.e, pub_key.n)
        block = rsa.transform.int2bytes(encrypted, keylength)

        return block

if __name__ == '__main__':
    account = Account()
    account.login()