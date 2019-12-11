# -*- coding: UTF-8 -*-
import os
import sys
import OCR_CODE
# 安装lxml
from bs4 import BeautifulSoup
import requests
import RW_ACCOUNT
import base64
import CATCH_PUBLIC_COURSE as pub

# 登录基本信息
class ZUCC:
    MainURL = "http://xk.zucc.edu.cn/default2.aspx"
    InitHeader = {"Host": "xk.zucc.edu.cn", "Connection": "keep-alive",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    CheckCodeURL = "http://xk.zucc.edu.cn/CheckCode.aspx?"
    CheckCodeHeader = ""
    PlanCourageURL = "http://xk.zucc.edu.cn/xsxk.aspx"
    # xs_main="http://xk.zucc.edu.cn/xs_main.aspx"

# 登录账号POST



class Account:
    def __init__(self):
        self.session = requests.Session()
        self.soup = None
        self.POSTDate = dict(__LASTFOCUS="",
                             __VIEWSTATE="随机码",
                             __VIEWSTATEGENERATOR="9BD98A7D", __EVENTTARGET="", __EVENTARGUMENT="", txtUserName="",
                             TextBox2="", txtSecretCode="-1", RadioButtonList1="%E5%AD%A6%E7%94%9F",
                             Button1="%E7%99%BB%E5%BD%95")
        self.account_data = RW_ACCOUNT.read_account()
        self.POSTDate["txtUserName"] = self.account_data["username"]
        self.POSTDate["TextBox2"] = self.account_data["password"]
        self.name = ""
        self.name_base64 = None

    def __refresh_code(self):
        # 获取验证码
        image_response = self.session.get(ZUCC.CheckCodeURL, stream=True)
        image = image_response.content
        if sys.platform == "linux":
            img_dir=os.getcwd()+"/"
        else:
            img_dir = os.getcwd() + "\\"
        print("###Saved in " + img_dir + "code.gif")
        try:
            with open(img_dir + "code.gif", "wb") as code_gif:
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
        print("##Get init page")
        while True:
            init_response = self.session.get(url=ZUCC.MainURL, headers=ZUCC.InitHeader)
            if init_response.ok:
                print("##GET login page succeed!")
                break
        login_soup = BeautifulSoup(init_response.text, "lxml")
        self.POSTDate["__VIEWSTATE"] = login_soup.find('input', attrs={'name': '__VIEWSTATE'})["value"]
        print("###GET StateCode:", self.POSTDate["__VIEWSTATE"])  # 随机码
        print("###GET checkCode")
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
                # self.name_base64 = base64.b64encode(self.name.encode('gb2312'))
                # print(self.name_base64)
                return
            else:
                try_time += 1
        print("#Check account password and restart!")

    def get_plan_course_page(self):
        url = ZUCC.PlanCourageURL+"?xh="+self.account_data["username"]+"&xm="+str(self.name_base64,encoding="utf8")+"&gnmkdm=N121101"
        header = ZUCC.InitHeader
        header["Referer"] = ZUCC.PlanCourageURL + "?xh=" + self.account_data["username"]
        # header["Upgrade-Insecure-Requests"] = "1"
        data = dict()
        data["gnmkdm"] = "N121101"
        data["xh"] = self.account_data["username"]
        data["xm"] = self.name_base64
        print(url)
        print(data)
        print(header)
        response = self.session.get(url=url, headers=header)
        # response = self.session.get(url=url, params=data,headers=header)

        print()
        print(response.text)
        # self.soup = BeautifulSoup(response, "lxml")
        # print(self.soup.find("title"))


    def get_public_course_page(self):
        pass

    def get_soup(self):
        return self.soup

    def get_session(self):
        return self.session


if __name__ == "__main__":
    me = Account()
    me.login()
    # me.get_plan_course_page()
    # pub.get_course(me)
