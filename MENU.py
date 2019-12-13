class MENU:
    """给这个类传入一个字典，可以输出一个菜单,执行get_key()可以取得一个用户输入值"""

    def __init__(self, menu_dic):
        self.menu_dic = menu_dic

    def print_list(self):
        for _key in self.menu_dic:
            print("[" + _key + "]: " + self.menu_dic[_key])