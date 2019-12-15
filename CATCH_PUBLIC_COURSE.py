from bs4 import BeautifulSoup
import time
import MENU


class info:
    InitHeader = {"Host": "xk.zucc.edu.cn", "Connection": "keep-alive",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    rules_page = "http://xk.zucc.edu.cn/sm_qxxxk.aspx"
    public_course_page_main = "http://xk.zucc.edu.cn/xf_xsqxxxk.aspx"


class PublicCourse:
    def __init__(self, account):
        self.account = account
        self.course_list = []
        self.num_of_selected = 0
        self.num_of_courses = 0

    def get_public_page(self):
        url = info.public_course_page_main + "?xh=" + self.account.account_data["username"]
        header = info.InitHeader
        header["Referer"] = url
        response = self.account.session.get(url=url, headers=header)
        time.sleep(3.5)
        if response.url != url:
            print('dismissing the rule')
            response = self.read_rules(response)
        soup = BeautifulSoup(response.text, "lxml")
        POSTData = {
            "__EVENTTARGET": "dpkcmcGrid$txtPageSize",
            "__VIEWSTATE": soup.find("input", type="hidden", id="__VIEWSTATE").get("value"),
            "__VIEWSTATEGENERATOR": soup.find("input", type="hidden", id="__VIEWSTATEGENERATOR").get("value"),
            "dpkcmcGrid$txtChoosePage": "1",
            "dpkcmcGrid$txtPageSize": "200"
        }
        response = self.account.session.post(url=response.url, data=POSTData)
        print("------get_public_page success------")
        return response

    def read_rules(self, response):
        url = info.rules_page + "?xh=" + self.account.account_data["username"]
        header = info.InitHeader
        header["Referer"] = url
        time.sleep(3.5)
        response = self.account.session.get(url=url, headers=header)
        soup = BeautifulSoup(response.text, "lxml")
        POSTDate = {
            "__VIEWSTATE": soup.find("input", id="__VIEWSTATE").get("value"),
            "__VIEWSTATEGENERATOR": soup.find("input", id="__VIEWSTATEGENERATOR").get("value"),
            "button1": "我已认真阅读，并同意以上内容",
            "TextBox1": 0
        }
        response = self.account.session.post(url=url, data=POSTDate)
        return response

    def get_the_message_of_page(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.find_all("tr")

        for num, link in enumerate(links[1:]):
            try:
                tds = link.find_all("td")
                name = tds[2].text
                code = tds[3].text
                teacher = tds[4].text
                time = tds[5].text
                margin = tds[11].text
                if time == "校区":
                    break
                lessen = PublicCourseInfo(num + 1, name, code, teacher, time, margin)
                self.course_list.append(lessen)
            except BaseException:
                break

        return

    def catch_course(self, response):
        number = str(int(input("输入想要抢的课程编号(课程编号即为第一项序号)\n退出程序输入数字‘0’\n>>>")) + 1)
        if number == "1":
            return
        url = info.public_course_page_main + "?xh=" + self.account.account_data["username"]
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
        while True:
            print("当前正在抢 " + self.course_list[int(number) - 2].name)
            response = self.account.session.post(url=url, data=POSTData)
            if self.num_of_selected_courses(response) == (self.num_of_selected + 1):
                print("抢课成功！！！！")
                self.num_of_selected += 1
                return
            else:
                try:
                    reason = "错误原因：" + BeautifulSoup(response.text, 'lxml').find('script').text.split('\'')[1]
                except BaseException:
                    reason = "错误原因：未知或已抢课成功"
                print("抢课失败！\t"
                      + reason
                      + "\t已选课程数量" + str(self.num_of_selected))


    def num_of_selected_courses(self, response):
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

    def search(self):
        search_dic = {
            "序号": "关键词类型",
            "1": "课程名称",
            "2": "教师",
            "3": "时间"
        }
        search_dic_menu = MENU.MENU(search_dic)
        search_dic_menu.print_list()
        n = input(">>>")
        key = input("输入查询信息：")
        if n == "1":
            for lesson in self.course_list:
                if key in lesson.name:
                    lesson.show_course_info()
        elif n == "2":
            for lesson in self.course_list:
                if key in lesson.teacher:
                    lesson.show_course_info()
        elif n == "3":
            for lesson in self.course_list:
                if key in lesson.time:
                    lesson.show_course_info()
        return

    def run(self):
        response = self.get_public_page()
        self.get_the_message_of_page(response)
        dic_of_public = {
            "1": "列出所有课表",
            "2": "按类型搜索内容",
            "0": "退出"
        }
        dic_of_public_menu=MENU.MENU(dic_of_public)
        dic_of_public_menu.print_list()
        while True:
            n = input(">>>")
            if n == "1":
                for lessen in self.course_list:
                    lessen.show_course_info()
                break
            elif n == "2":
                self.search()
                break
            elif n == "0":
                return
            print("请输入正确的序号")
        self.num_of_selected = self.num_of_selected_courses(response)
        print("已选课程数量：" + str(self.num_of_selected))
        self.catch_course(response)
        pass


class PublicCourseInfo:
    def __init__(self, num, name, code, teacher, time, margin):
        self.num = str(num)
        self.name = str(name)
        self.code = str(code)
        self.teacher = str(teacher)
        self.time = str(time)
        self.margin = str(margin)

    def show_course_info(self):
        print("课程编号:" + self.num
              + "\t课程名称:" + self.name
              + "\t课程代码:" + self.code
              + "\t课程教师:" + self.teacher
              + "\t课程时间:" + self.time
              + "\t课程余量:" + self.margin)

    def __contains__(self, item):
        if item in self:
            return True
        else:
            return False


