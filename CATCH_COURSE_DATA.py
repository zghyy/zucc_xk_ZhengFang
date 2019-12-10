import LOGIN
from bs4 import BeautifulSoup
import requests


class CourseSpider:
    def __init__(self):
        self.me = LOGIN.Account()

    def catch_plan_course_page(self):
        self.me.login()
        soup = self.me.get_soup()
        for item in


if __name__ == "__main__":
    spider = CourseSpider()
    spider.catch_plan_course_page()
