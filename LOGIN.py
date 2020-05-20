# -*- coding: UTF-8 -*-
import os
import sys
import OCR_CODE
from bs4 import BeautifulSoup
import requests
import RW_ACCOUNT

# zucc正方教务系统需要用到的一些网站连接以及初始化的抢课数据包
class ZUCC:
    DOMAIN = "xk.zucc.edu.cn"
    MainURL = "http://xk.zucc.edu.cn/default2.aspx"
    InitHeader = {"Host": "xk.zucc.edu.cn", "Connection": "keep-alive",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    CheckCodeURL = "http://xk.zucc.edu.cn/CheckCode.aspx?"
    CheckCodeHeader = ""
    PlanCourageURL = "http://xk.zucc.edu.cn/xsxk.aspx"
    xsmain="http://xk.zucc.edu.cn/xs_main.aspx"

# Account为登录用的账户
class Account:
    def __init__(self, name=None, password=None):
        self.session = requests.Session()
        self.soup = None
        self.POSTDate = {'__LASTFOCUS': "", '__VIEWSTATE': "随机码", '__VIEWSTATEGENERATOR': "9BD98A7D",
                         '__EVENTTARGET': "", '__EVENTARGUMENT': "", 'txtUserName': "", 'TextBox2': "",
                         'txtSecretCode': "-1", 'RadioButtonList1': "%E5%AD%A6%E7%94%9F",
                         'Button1': "%E7%99%BB%E5%BD%95"}
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
        image_response = self.session.get(ZUCC.CheckCodeURL, stream=True)
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

    # 登录进入主页
    def login(self):
        print("#Begin to login")
        # print("##Get init page")
        while True:
            init_response = self.session.get(url=ZUCC.MainURL, headers=ZUCC.InitHeader)
            if init_response.ok:
                print("##GET login page succeed!")
                break
        login_soup = BeautifulSoup(init_response.text, "lxml")
        self.POSTDate["__VIEWSTATE"] = login_soup.find('input', attrs={'name': '__VIEWSTATE'})["value"]
        # print("###GET StateCode:", self.POSTDate["__VIEWSTATE"])  # 随机码
        # print("###GET checkCode")
        self.__get_check_code_ocr()
        print("##POST login")
        try_time = 0
        while try_time < 300:
            login_response = self.session.post(ZUCC.MainURL, data=self.POSTDate)
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
