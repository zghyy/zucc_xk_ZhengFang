from flask import Flask
from flask import render_template
from flask import request
import LOGIN

# 实例化，可视为固定格式
app = Flask(__name__)


# 配置路由，当请求get.html时交由get_html()处理
@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/deal_request', methods=['POST'])
def deal_request():
    name = request.form["xh"]
    password = request.form["mm"]
    me = LOGIN.Account(name,password)
    me.login()
    if me.name=="":
        return render_template("result.html", result="登录失败，请确认账号密码", name=me.name)
    else:
        return render_template("result.html", result="登录成功",name=me.name)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
