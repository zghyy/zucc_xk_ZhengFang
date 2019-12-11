from bs4 import BeautifulSoup
import time
class info:
    InitHeader = {"Host": "xk.zucc.edu.cn", "Connection": "keep-alive",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    rules_page = "http://xk.zucc.edu.cn/sm_qxxxk.aspx"
    public_course_page_main="http://xk.zucc.edu.cn/xf_xsqxxxk.aspx"


def get_course(account):
    response=get_public_page(account)
    # show_the_message_of_page(response)
    pass

def get_public_page(account):
    url = info.public_course_page_main+"?xh="+account.account_data["username"]
    header = info.InitHeader
    header["Referer"]=url
    response=account.session.get(url=url,headers=header)
    time.sleep(3.5)
    if response.url != url:
        response=read_rules(account)
    time.sleep(3.5)
    #------get_public_page success------
    print("------get_public_page success------")
    soup=BeautifulSoup(response.text,"lxml")
    # print(soup.text)
    POSTData={
        "__EVENTTARGET":"dpkcmcGrid$txtPageSize",
        "__VIEWSTATE":soup.find("input",type="hidden",id="__VIEWSTATE").get("value"),
        "__VIEWSTATEGENERATOR": soup.find("input",type="hidden", id="__VIEWSTATEGENERATOR").get("value"),
        "dpkcmcGrid$txtChoosePage":"1",
        "dpkcmcGrid$txtPageSize":"200"
    }
    response=account.session.post(url=response.url,data=POSTData)
    # print(response.text)
    # print(response.url)
    return response

def read_rules(account):
    url = info.rules_page+"?xh="+account.account_data["username"]
    header = info.InitHeader
    header["Referer"]=url
    response=account.session.get(url=url,headers=header)
    # print(response.text)
    soup=BeautifulSoup(response.text,"lxml")
    POSTDate={
          "__VIEWSTATE":soup.find("input",id="__VIEWSTATE").get("value"),
          "__VIEWSTATEGENERATOR":soup.find("input",id="__VIEWSTATEGENERATOR").get("value"),
          "button1":"我已认真阅读，并同意以上内容",
          "TextBox1":0
    }
    response = account.session.post(url=url, data=POSTDate)
    print(response.text)
    return response

def show_the_message_of_page(response):
    soup=BeautifulSoup(response.text,"lxml")
    links=soup.find_all("tr")
    for link in links:
        print(link.children.text)
