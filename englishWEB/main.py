# coding=utf-8 

from flask import Flask, render_template, request, session, current_app
from youdao import *
# encoding=utf8  
import sys  
  
reload(sys)  
sys.setdefaultencoding('utf8')  
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    return render_template('base.html')


@app.route('/dic', methods=['POST', 'GET'])
def dic():
    word = request.form.get('word')
    uname = request.form.get('uname')
    # print(word)
    # print(uname)

#   处理异常查询迎合前端
    if len(attack_YD(word)) > 2:
        return attack_YD(word)

    result, sw = attack_YD(word)
    print(sw)
    return render_template('result.html', result=result, origin=word, uname=uname, sw=sw)


@app.route('/favicon.ico')
def get_fav():
    # print(__name__)
    return current_app.send_static_file('/static/favicon.ico')


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
