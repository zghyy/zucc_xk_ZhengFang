import sys
print("\033[1;31;40m"+sys.platform+"\033[0m")
print("1"+"\t"+"2")
class course_info:
    def __init__(self, num, name, code, teacher, time):
        self.num = num
        self.name = name
        self.code = code
        self.teacher = teacher
        self.time = time

    def show_course_info(self):
        print("编号:" + self.num
              + "\t课程名称:" + self.name
              + "\t课程代码:" + self.code
              + "\t课程教师:" + self.teacher
              + "\t课程时间:" + self.time)

# lesson=course_info("1","1","1","1","1")
# lesson.show_course_info()
n="2"
print(n.zfill(3))
