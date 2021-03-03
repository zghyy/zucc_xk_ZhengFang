import time
import LOGIN
from bs4 import BeautifulSoup


class EnglishCourse:
    def __init__(self, account):
        self.account = account
        self.urls = []
        self.course_list=[]

    def choose_course_class(self, response):
        self.account.soup = BeautifulSoup(response.text, "lxml")
        links = self.account.soup.find_all(name="tr")
        for num, link in enumerate(links[1:-1]):
            tds = link.find_all("td")
            print("编号：" + str(num + 1) + "\t课程名称: " + tds[1].text)
            url = "http://" + LOGIN.ZUCC.DOMAIN + "/clsPage/xsxjs.aspx?" + "xkkh=" + \
                  tds[1].find("a").get("onclick").split("=")[1][0:-3] + "&xh=" + self.account.account_data["username"]
            self.urls.append(url)
        n = input("输入编号：")
        url = self.urls[int(n) - 1]
        self.obj_url = url
        header = LOGIN.ZUCC.InitHeader
        header["Referer"] = "http://xk.zucc.edu.cn/xs_main.aspx?xh=" + self.account.account_data['username']
        item_response = self.account.session.get(url=url, headers=header)
        item_soup = BeautifulSoup(item_response.text, "lxml")
        self.obj_viewstate = item_soup.find_all(name='input', id="__VIEWSTATE")[0]["value"]
        item_trs = item_soup.find_all(name="tr")
        for num, item_tr in enumerate(item_trs[1:]):
            try:
                tds = item_tr.find_all("td")
                code = tds[0].find('input').get('value')
                teacher = tds[2].text
                time = tds[3].text
                lessen = EnglishCourseInfo(num + 1, code, teacher, time)
                self.course_list.append(lessen)
            except BaseException:
                return
        return

    def catch_course(self):
        for info in self.course_list:
            info.show_course_info()
        n = input("输入编号(0退出)：")
        while True:
            if n == "0":
                return
            elif int(n) < 0 or int(n) > len(self.course_list):
                print("请输入正确的数字")
            else:
                break
        post_data = {"__EVENTTARGET": "Button1",
                     "__VIEWSTATEGENERATOR": "55DF6E88",
                     "xkkh": self.course_list[int(n) - 1].code,
                     "__VIEWSTATE": self.obj_viewstate,
                     "RadioButtonList1": 1}
        while True:
            response = self.account.session.post(url=self.obj_url, data=post_data)
            soup = BeautifulSoup(response.text, "lxml")
            try:
                reply = soup.find('script').string.split("'")[1]
            except BaseException:
                reply = "未知错误"
            print(reply + "\t\t" + str(time.strftime('%m-%d-%H-%M-%S', time.localtime(time.time()))),flush=True)
            if reply == "选课成功！":
                return

    def enter_english_course(self):
        url = LOGIN.ZUCC.PlanCourageURL + "?xh=" + self.account.account_data["username"]
        header = LOGIN.ZUCC.InitHeader
        header["Referer"] = url
        response = self.account.session.get(url=url, headers=header)
        self.account.soup = BeautifulSoup(response.text, "lxml")
        post_data = {"__EVENTTARGET": "", "__EVENTARGUMENT": "", "__LASTFOCUS": "", "__VIEWSTATEGENERATOR": "4842AF95",
                     "xx": "", "Button3": "大学英语拓展课",
                     "__VIEWSTATE": self.account.soup.find(name='input', id="__VIEWSTATE")["value"]}
        response = self.account.session.post(url=url, data=post_data)
        return response

    def run(self):
        response = self.enter_english_course()
        self.choose_course_class(response)
        self.catch_course()

class EnglishCourseInfo:
    def __init__(self, num, code, teacher, time):
        self.num = str(num)
        self.code = str(code)
        self.teacher = str(teacher)
        self.time = str(time)

    def show_course_info(self):
        print("课程编号:" + self.num
              + "\t课程代码:" + self.code
              + "\t课程教师:" + self.teacher
              + "\t课程时间:" + self.time)

    def __contains__(self, item):
        if item in self:
            return True
        else:
            return False



if __name__ == '__main__':
    account = LOGIN.Account()
    account.login()
    english = EnglishCourse(account)
    english.run()
