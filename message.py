# encoding: utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

# 初始化一个 Flask 实例
app = Flask(__name__)
# message_list 用来存储所有的 message
message_list = []


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello Gatler'


@app.route('/message')
def message_view():
    return render_template('message_index.html', messages=message_list)


@app.route('/message/add', methods=['POST'])
def message_add():
    msg = {
        'content': request.form.get('msg_post', ''),
    }
    message_list.append(msg)
    return redirect('/message')


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
