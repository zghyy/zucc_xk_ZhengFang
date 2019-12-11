import LOGIN
from bs4 import BeautifulSoup
import requests


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

    def catch_information(self):
        url = LOGIN.ZUCC.PlanCourageURL + "?xh=" + self.account.account_data["username"] + "&xm=" + self.account.name + "&gnmkdm=N121101"
        header = LOGIN.ZUCC.InitHeader
        header["Referer"] = LOGIN.ZUCC.PlanCourageURL + "?xh=" + self.account.account_data["username"]
        response = self.account.session.get(url=url, headers=header)
        self.account.soup = BeautifulSoup(response.text, "lxml")

    def set_target_course(self):
        pass

    def attack(self):
        pass


if __name__ == "__main__":
    planned_course_spider = PlannedCourse()
    planned_course_spider.catch_information()
    # planned_course_spider.set_target_course()
    # planned_course_spider.attack()
