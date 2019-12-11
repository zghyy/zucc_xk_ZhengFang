from bs4 import BeautifulSoup
import time
import LOGIN


class info:
    InitHeader = {"Host": "xk.zucc.edu.cn", "Connection": "keep-alive",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    rules_page = "http://xk.zucc.edu.cn/sm_qxxxk.aspx"
    public_course_page_main = "http://xk.zucc.edu.cn/xf_xsqxxxk.aspx"


class PublicCourse:
    def __init__(self, account):
        self.account = account
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
        response = self.account.session.post(url=response.url, data=POSTData)
        # print(response.text)
        # print(response.url)
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
        # print(response.text)
        return response

    def get_the_message_of_page(self, response):
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
                lessen = CourseInfo(num + 1, name, code, teacher, time)
                course_list.append(lessen)
            except BaseException:
                break
        # print("-------following courses--------")

        # for lessen in course_list:
        #     lessen.show_course_info()
        return course_list

    def catch_course(self, course_list, response):
        number = str(int(input("输入想要抢的课程编号(课程编号即为第一项序号)\n"))+1)
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
        print(POSTData)
        while True:
            print("当前正在抢 "+course_list[int(number)-2].name)
            response = self.account.session.post(url=url, data=POSTData)
            if self.num_of_selected_courses(response) == self.num_of_selected + 1:
                self.num_of_selected += 1
                break
            else:
                print("抢课失败！\t已选课程数量" + str(self.num_of_selected))
        # return response

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

    def run(self):
        response = self.get_public_page()
        course_list = self.get_the_message_of_page(response)

        print("-------following courses--------")
        for lessen in course_list:
            lessen.show_course_info()

        self.num_of_selected = self.num_of_selected_courses(response)
        self.catch_course(course_list, response)
        pass


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


if __name__ == '__main__':
    account = LOGIN.Account()
    account.login()
    public = PublicCourse(account)
    public.run()
