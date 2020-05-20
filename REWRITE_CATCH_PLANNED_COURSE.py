import LOGIN
from bs4 import BeautifulSoup


class RE_PlannedCourse:
    def __init__(self, account):
        self.account = account
        # 最终选择的课程种类的url
        self.obj_url = ""
        # 所有课程种类的url
        self.urls = []

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
        print(BeautifulSoup(item_response.text, 'lxml'))
        return

    def run(self):
        # 进入计划内选课界面
        response = self.enter_planned_course()
        # 爬取课程信息
        self.choose_course_class(response)
        # 模拟发包抢课
        self.catch_course()


if __name__ == '__main__':
    account = LOGIN.Account()
    account.login()
    planned = RE_PlannedCourse(account)
    planned.run()
