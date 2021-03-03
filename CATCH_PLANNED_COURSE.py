import LOGIN
from bs4 import BeautifulSoup
import time


class PlannedCourse:
    def __init__(self, account):
        self.account = account
        # 最终选择的课程种类的url
        self.obj_url = ""
        # 所有课程种类的url
        self.urls = []
        # 所有开课信息
        self.course_list = []
        # 发送选课数据包的时候要用到
        self.obj_viewstate = ""

    def enter_planned_course(self):
        url = LOGIN.ZUCC.PlanCourageURL + "?xh=" + self.account.account_data["username"]
        header = LOGIN.ZUCC.InitHeader
        header["Referer"] = url
        response = self.account.session.get(url=url, headers=header)
        """以下两行代码可以用先解析以下，看下当前是否在我们需要的页面"""
        # self.account.soup = BeautifulSoup(response.text, "lxml")
        # print(self.account.soup)
        return response

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
                reply = "未知错误或者已选上课程"
            print(reply + "\t\t" + str(time.strftime('%m-%d-%H-%M-%S', time.localtime(time.time()))),flush=True)
            if reply == "选课成功！":
                return

    def choose_course_class(self, response):
        self.account.soup = BeautifulSoup(response.text, "lxml")
        links = self.account.soup.find_all(name="tr")
        for num, link in enumerate(links[1:-1]):
            tds = link.find_all("td")
            print("编号：" + str(num + 1) + "\t课程名称: " + tds[1].text)
            url = "http://" + LOGIN.ZUCC.DOMAIN + "/clsPage/xsxjs.aspx?" + "xkkh=" + \
                  tds[1].find("a").get("onclick").split("=")[1][0:-3] + "&xh=" + self.account.account_data["username"]
            # print(url)
            self.urls.append(url)

        n = input("输入编号：")
        url = self.urls[int(n) - 1]
        self.obj_url = url
        header = LOGIN.ZUCC.InitHeader
        header["Referer"] = "http://xk.zucc.edu.cn/xs_main.aspx?xh=" + self.account.account_data['username']
        item_response = self.account.session.get(url=url, headers=header)
        # print(BeautifulSoup(item_response.text, 'lxml'))
        item_soup = BeautifulSoup(item_response.text, "lxml")
        self.obj_viewstate = item_soup.find_all(name='input', id="__VIEWSTATE")[0]["value"]
        item_trs = item_soup.find_all(name="tr")
        for num, item_tr in enumerate(item_trs[1:]):
            try:
                tds = item_tr.find_all("td")
                code = tds[0].find('input').get('value')
                teacher = tds[2].text
                time = tds[3].text
                lessen = PlannedCourseInfo(num + 1, code, teacher, time)
                self.course_list.append(lessen)
            except BaseException:
                return
        return

    def run(self):
        # 进入计划内选课界面
        response = self.enter_planned_course()
        # 爬取课程信息
        self.choose_course_class(response)
        # 模拟发包抢课
        self.catch_course()


class PlannedCourseInfo:
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
    planned = PlannedCourse(account)
    planned.run()
