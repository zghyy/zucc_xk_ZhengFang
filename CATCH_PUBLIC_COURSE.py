from bs4 import BeautifulSoup
import time


class info:
    InitHeader = {"Host": "xk.zucc.edu.cn", "Connection": "keep-alive",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    rules_page = "http://xk.zucc.edu.cn/sm_qxxxk.aspx"
    public_course_page_main = "http://xk.zucc.edu.cn/xf_xsqxxxk.aspx"


def get_course(account):
    response = get_public_page(account)
    course_list = show_the_message_of_page(response)
    response = catch_course(account, course_list, response)
    num = num_of_selected_courses(response)
    pass


def get_public_page(account):
    url = info.public_course_page_main + "?xh=" + account.account_data["username"]
    header = info.InitHeader
    header["Referer"] = url
    response = account.session.get(url=url, headers=header)
    time.sleep(3.5)
    if response.url != url:
        print('dismissing the rule')
        response = read_rules(account, response)
    # ------get_public_page success------
    print("------get_public_page success------")
    soup = BeautifulSoup(response.text, "lxml")
    POSTData = {
        "__EVENTTARGET": "dpkcmcGrid$txtPageSize",
        "__VIEWSTATE": soup.find("input", type="hidden", id="__VIEWSTATE").get("value"),
        "__VIEWSTATEGENERATOR": soup.find("input", type="hidden", id="__VIEWSTATEGENERATOR").get("value"),
        "dpkcmcGrid$txtChoosePage": "1",
        "dpkcmcGrid$txtPageSize": "200"
    }
    response = account.session.post(url=response.url, data=POSTData)
    # print(response.text)
    # print(response.url)
    return response


def read_rules(account, response):
    url = info.rules_page + "?xh=" + account.account_data["username"]
    header = info.InitHeader
    header["Referer"] = url
    time.sleep(3.5)
    response = account.session.get(url=url, headers=header)
    soup = BeautifulSoup(response.text, "lxml")
    POSTDate = {
        "__VIEWSTATE": soup.find("input", id="__VIEWSTATE").get("value"),
        "__VIEWSTATEGENERATOR": soup.find("input", id="__VIEWSTATEGENERATOR").get("value"),
        "button1": "我已认真阅读，并同意以上内容",
        "TextBox1": 0
    }
    response = account.session.post(url=url, data=POSTDate)
    # print(response.text)
    return response


def show_the_message_of_page(response):
    course_list = []
    soup = BeautifulSoup(response.text, "lxml")
    links = soup.find_all("tr")

    for num, link in enumerate(links[1:]):
        try:
            tds = link.find_all("td")
            name = tds[2].text
            code = tds[3].text
            teacher = tds[4].text
            time = tds[5].text
            if time == "校区":
                break
            lessen = CourseInfo(num, name, code, teacher, time)
            course_list.append(lessen)
        except BaseException:
            break
    print("-------following courses--------")

    for lessen in course_list:
        lessen.show_course_info()
    return course_list


def catch_course(account, course_list, response):
    number = str(input("输入想要抢的课程编号(课程编号即为第一项序号)\n"))
    url = info.public_course_page_main + "?xh=" + account.account_data["username"]
    soup = BeautifulSoup(response.text, "lxml")
    POSTData = {
        "__EVENTTARGET": "dpkcmcGrid$txtPageSize",
        "__VIEWSTATE": soup.find("input", type="hidden", id="__VIEWSTATE").get("value"),
        "__VIEWSTATEGENERATOR": soup.find("input", type="hidden", id="__VIEWSTATEGENERATOR").get("value"),
        "dpkcmcGrid$txtChoosePage": "1",
        "dpkcmcGrid$txtPageSize": "200",
        "Button1": "立即提交"
    }
    POSTData["kcmcGrid$ctl" + number.zfill(2) + "$xk"] = "on"
    POSTData["kcmcGrid$ctl" + number.zfill(2) + "$jc"] = "on"
    # while True:
    response = account.session.post(url=url, data=POSTData)
    #     if num_of_selected_courses(response)
    # print(response.text)
    return response


def num_of_selected_courses(response):
    soup = BeautifulSoup(response.text, "lxml")
    links = soup.find_all("tr")
    number = 0
    for link in links[1:]:
        try:
            tds = link.find_all("td")
            tmp = tds[5].text
            number = number + 1
            if tmp == "校区":
                number = 0
        except BaseException:
            break
    return number


class CourseInfo:
    def __init__(self, num, name, code, teacher, time):
        self.num = str(num)
        self.name = str(name)
        self.code = str(code)
        self.teacher = str(teacher)
        self.time = str(time)

    def show_course_info(self):
        print("课程编号:" + self.num
              + "\t课程名称:" + self.name
              + "\t课程代码:" + self.code
              + "\t课程教师:" + self.teacher
              + "\t课程时间:" + self.time)
