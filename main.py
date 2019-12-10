import RW_ACCOUNT
import CATCH_COURSE_DATA


class MENU:
    key = 0
    key_range = 4
    item = [
        "设置账号密码",
        "设置目标课程",
        "抓取课程数据",
        "开始抢课",
    ]

    def print_list(self):
        i = 1
        for x in self.item:
            print("[", i, "]" + x)
            i += 1
        print("[ 0 ]退出程序")
        self.key_range = i - 1

    def get_key(self):
        while True:
            self.key = int(input("input-number>>"))
            if self.key > self.key_range or self.key < 0:
                print("无效的参数")
                continue
            print("select:", self.item[self.key-1])
            if self.key == 0:
                return
            elif self.key == 1:
                RW_ACCOUNT.set_account()
            elif self.key == 2:
                pass
            elif self.key == 3:
                pass
            elif self.key == 4:
                pass


if __name__ == "__main__":
    begin_menu = MENU()
    begin_menu.print_list()
    begin_menu.get_key()
