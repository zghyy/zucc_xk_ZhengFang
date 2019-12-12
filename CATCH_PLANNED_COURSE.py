from bs4 import BeautifulSoup
import copy
import time
import json
import LOGIN
import MENU


class PlannedCourseInfo:
    def __init__(self, main_num, name, code, margin, detail):
        self.num = str(main_num)
        self.name = str(name)
        self.code = str(code)
        self.margin = str(margin)
        self.detail = copy.deepcopy(detail)

    def show_course_summary(self):
        print("主编号:" + self.num
              + "\t名称:" + self.name
              + "\t代码:" + self.code
              + "\t总余量:" + self.margin)

    def show_course_info(self):
        for item in self.detail:
            print("       ∟____ 辅编号:" + item["secondary_num"] + "\t教师:" + item["teacher"]
                  + "\t时间:" + item["time"] + "\t余量:" + item["margin"])


class PlannedCourse:
    """
    思路：
        1：登录
        2：进入选课界面
        3：抓取课程信息并保存
        4：用户输入想要抢的一门或几门课程
        5：开始抢课
    """

    def __init__(self):
        # 开始登录
        self.account = LOGIN.Account()
        self.account.login()
        self.english_course = []
        self.target_english_course = []

    def init_menu(self):
        menu_dic = {
            "1": "本专业课程",
            "2": "大学英语扩展课",
            "0": "退出",
        }
        menu = MENU.MENU(menu_dic=menu_dic)
        menu.print_list()
        while True:
            _key = input(">>>")
            if _key == "1":
                self.catch_professional_course()
            elif _key == "2":
                # 设置计划内课程target
                self.catch_english_course()
                print("输入课程编号选择课程，0返回")
                for item in self.english_course:
                    item.show_course_summary()
                    # item.show_course_info()
                length = len(self.english_course)
                while True:
                    i_key = input("(主编号)>>>")
                    if 0 < int(i_key) <= length:
                        print("你选择了", self.english_course[int(i_key) - 1].name)
                        self.english_course[int(i_key) - 1].show_course_info()
                        item_length = len(self.english_course[int(i_key) - 1].detail)
                        while True:
                            j_key = input("(辅编号)>>>")
                            if 1 <= int(j_key) <= item_length:
                                detail = self.english_course[int(i_key) - 1].detail[int(j_key) - 1]
                                print("你选择了: 辅编号:", detail["secondary_num"], "\t教师:", detail["teacher"]
                                      , "\t时间:", detail["time"], "\t余量:", detail["margin"])
                                tmp = {i_key: j_key}
                                self.target_english_course.append(tmp)
                                break
                            elif int(j_key) == 0:
                                break
                            else:
                                print("请输入正确的数字")

                    elif i_key == 0:
                        break
                    else:
                        print("请输入正确的数字")
            elif _key == "0":
                return
            else:
                print("请输入正确的数字")

    def __catch_view_state(self):
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

    def catch_professional_course(self):
        pass

    def __enter_english_page(self):
        self.__catch_view_state()
        url = LOGIN.ZUCC.PlanCourageURL + "?xh=" + self.account.account_data["username"]
        post_data = {"__EVENTTARGET": "", "__EVENTARGUMENT": "", "__LASTFOCUS": "", "__VIEWSTATEGENERATOR": "4842AF95",
                     "zymc": "0121%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6%E4%B8%8E%E6%8A%80%E6%9C%AF%E4%B8%BB%E4%BF%AE%E4%B8%93%E4%B8%9A%7C%7C2019",
                     "xx": "", "Button3": "大学英语拓展课",
                     "__VIEWSTATE": self.account.soup.find(name='input', id="__VIEWSTATE")["value"]}
        response = self.account.session.post(url=url, data=post_data)
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.find_all(name="tr")
        return links

    def catch_english_course(self):
        links = self.__enter_english_page()
        planned_course_file = open("planned_course.json", "r")
        detail_list = json.load(planned_course_file)
        planned_course_file.close()
        i = 1
        for link in links[1:-1]:
            tmp = link.find_all("td")
            # print(tmp[0].find(name="a").text, tmp[1].find(name="a").text, tmp[9].text)
            self.english_course.append(
                PlannedCourseInfo(i, tmp[1].find(name="a").text, tmp[0].find(name="a").text,
                                  tmp[9].text, detail_list[i - 1]))
            i += 1

    def update_course(self):
        links = self.__enter_english_page()
        detail_list = []
        for link in links[1:-1]:
            tmp = link.find_all("td")
            detail = []
            url = "http://" + LOGIN.ZUCC.DOMAIN + tmp[0].find(name="a")["onclick"][21:-8]
            header = LOGIN.ZUCC.InitHeader
            header["Referer"] = "http://xk.zucc.edu.cn/xs_main.aspx?xh=31901040"
            time.sleep(4)
            item_response = self.account.session.get(url=url, headers=header)
            item_soup = BeautifulSoup(item_response.text, "lxml")
            item_trs = item_soup.find_all(name="tr")
            j = 1
            for item_tr in item_trs[1:-1]:
                tds = item_tr.find_all("td")
                detail_td = {"secondary_num": str(j), "code": tds[0].find(name="input")["value"],
                             "teacher": tds[2].find(name="a").text,
                             "time": tds[3].text,
                             "margin": str(int(tds[11].text) - int(tds[13].text)) + "/" + tds[11].text}
                detail.append(detail_td)
                j += 1
            detail_list.append(detail)
        # 缓存在文件
        planned_course_file = open("planned_course.json", "w")
        planned_course_file.write(json.dumps(detail_list))
        planned_course_file.close()

    def attack(self):
        if len(self.target_english_course) < 1:
            print("未选择任何课程，请先选择课程")
            return
        for number in self.target_english_course:
            pass


if __name__ == "__main__":
    planned_course_spider = PlannedCourse()
    planned_course_spider.init_menu()
    # planned_course_spider.attack()
    # planned_course_spider.catch_english_course()
    # planned_course_spider.update_course()
