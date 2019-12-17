import LOGIN
from bs4 import BeautifulSoup
import time


class OutPlannedCourse:
    def __init__(self, account):
        self.account = account
        self.urls=[]
        self.obj_url=""
        self.obj_viewstate=""
        self.course_list = []



    def __catch_view_state(self):
        """抓取 HTML中的 VIEWSTATE"""
        url = LOGIN.ZUCC.PlanCourageURL + "?xh=" + self.account.account_data[
            "username"] + "&xm=" + self.account.name + "&gnmkdm=N121101"
        header = LOGIN.ZUCC.InitHeader
        header["Referer"] = LOGIN.ZUCC.PlanCourageURL + "?xh=" + self.account.account_data["username"]
        response = self.account.session.get(url=url, headers=header)
        while response.status_code == 302:
            response = self.account.session.get(url=url, headers=header)
            time.sleep(0.2)
        self.account.soup = BeautifulSoup(response.text, "lxml")
        # print(response.status_code)

    def enter_out_planned_course(self):
        self.__catch_view_state()
        url = LOGIN.ZUCC.PlanCourageURL + "?xh=" + self.account.account_data["username"]
        post_data = {"__EVENTTARGET": "zymc", "__EVENTARGUMENT": "", "__LASTFOCUS": "",
                     "__VIEWSTATEGENERATOR": "4842AF95",
                     "zymc": "0121计算机科学与技术主修专业||2019", "xx": "",
                     "__VIEWSTATE": self.account.soup.find(name='input', id="__VIEWSTATE")["value"]}
        response = self.account.session.post(url=url, data=post_data)
        return response


    def choose_course_class(self,response):
        self.account.soup = BeautifulSoup(response.text, "lxml")
        links = self.account.soup.find_all(name="tr")
        for num,link in enumerate(links[1:-1]):
            tds = link.find_all("td")
            print("编号："+str(num+1)+"\t课程名称"+tds[1].text)
            url = "http://" + LOGIN.ZUCC.DOMAIN + "/clsPage/xsxjs.aspx?" + "xkkh=" + \
                  tds[1].find("a").get("onclick").split("=")[1][0:-3] + "&xh=" + self.account.account_data["username"]
            # print(url)
            self.urls.append(url)
        n=input("输入编号：")
        url=self.urls[int(n)-1]
        self.obj_url=url
        header = LOGIN.ZUCC.InitHeader
        header["Referer"] = "http://xk.zucc.edu.cn/xs_main.aspx?xh=" + self.account.account_data['username']
        item_response = self.account.session.get(url=url, headers=header)
        # print(item_response.url)
        item_soup = BeautifulSoup(item_response.text, "lxml")
        self.obj_viewstate=item_soup.find_all(name='input', id="__VIEWSTATE")[0]["value"]
        item_trs = item_soup.find_all(name="tr")
        for num,item_tr in enumerate(item_trs[1:]):
            try:
                tds = item_tr.find_all("td")
                code = tds[0].find('input').get('value')
                teacher = tds[2].text
                time = tds[3].text
                lessen = OutPlannedCourseInfo(num + 1, code, teacher, time)
                self.course_list.append(lessen)
            except BaseException:
                return

    def catch_course(self):
        for info in self.course_list:
            info.show_course_info()
        n=input("输入编号(0退出)：")
        while True:
            if n== "0":
                return
            elif int(n)<0 or int(n) >len(self.course_list):
                print("请输入正确的数字")
            else:
                break
        post_data = {"__EVENTTARGET": "Button1",
                     "__VIEWSTATEGENERATOR": "55DF6E88",
                     "RadioButtonList1": "1",
                     "xkkh": self.course_list[int(n)-1].code,
                     "__VIEWSTATE": self.obj_viewstate}

        while True:
            response = self.account.session.post(url=self.obj_url, data=post_data)
            soup = BeautifulSoup(response.text, "lxml")
            try:
                reply = soup.find(name="script").text.split("'")[1]
            except BaseException:
                reply = "未知错误"
            print(reply)
            if reply == "选课成功！":
                return

        # pass

    def run(self):
        response = outplanned.enter_out_planned_course()
        self.choose_course_class(response)
        self.catch_course()

class OutPlannedCourseInfo:
    def __init__(self, num, code, teacher, time):
        self.num = str(num)
        self.code = str(code)
        self.teacher = str(teacher)
        self.time = str(time)
        # self.margin = str(margin)

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
    outplanned = OutPlannedCourse(account)
    outplanned.run()
