from flask import Flask, request, render_template, redirect, session, jsonify
from flask_cors import CORS
import re

from routes.config import (
    tributary_list,
    videoURL,
    track_set,
    session_number,
    rules
)
from routes.verify import (
    generate_raw,
    en_vcode,
    de_vcode
)
from routes.sql import (
    connect_db,
    sqlOperation,
    sqlRead,
    sqlRead_status
)
from routes.score_sort import (
    score_sort
)

app = Flask(__name__)
CORS(app, resources=r'/*', supports_credentials=True)

app.secret_key = 'JASONCRYING'
app.config['PERMANENT_SESSION_LIFETIME'] = 7200


# home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html', msg='您好！')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    args = request.args
    if args.get('msg') is not None:
        msg = args['msg']
    if request.method == 'GET':
        return render_template("login.html", msg=msg)
    loginForm = request.form
    username = loginForm.get("username")
    pwd = loginForm.get("pass")
    language = loginForm.get("checkbox")
    if language not in ['CN', 'EN']:
        language = 'CN'
    sql = '''SELECT * FROM user_table'''
    result = sqlRead(sql)
    if result is None:
        return render_template("login.html", msg='连接数据库失败导致的登录异常！')
    # 验证登录信息
    loginFlag = 0
    for item in result:
        if username == item[1] and pwd == str(item[2]):
            loginFlag = 1
            break
    if loginFlag == 1:
        session['language'] = language
        session['user_info'] = username
        return redirect('/user/' + username)
    else:
        return render_template("login.html", msg='用户名或密码输入错误！')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'GET':
        return render_template('register.html')
    registerForm = request.form
    username = registerForm.get("username").strip()
    pwd = registerForm.get("pass").strip()
    confirm = registerForm.get("confirm").strip()
    if username == '' or pwd == '' or confirm == '' or \
            pwd != confirm:
        return redirect('/register')

    sql = '''INSERT INTO user_table (
        username,
        pwd
    ) VALUES(
        "%s",
        "%s"
    )''' % (username, pwd)
    msg = sqlOperation(sql)

    return redirect('/login'+'?msg='+msg)

@app.route('/user/<username>')
def admin(username):
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    return render_template("user.html", username=user_info, language=session['language'])
@app.route('/logout')
def logout():
    if session.get('user_info'):
        del session['user_info']
    return redirect('/login')
@app.route('/published', methods=['GET'])
def published():
    current_user = session.get('user_info')
    if not current_user:
        return jsonify({
            'ret_js': [],
            'current_user': ''
        })
    ret_js = []
    try:
        ret_js.extend(sqlRead_status(current_user))
    except Exception as e:
        if session.get('user_info'):
            del session['user_info']
        return jsonify({
            'ret_js': [],
            'current_user': ''
        })

    return jsonify({
        'ret_js': ret_js,
        'current_user': current_user
    })

@app.route('/submit', methods=['POST'])
def submit():
    current_user = session.get('user_info')
    if current_user is None:
        return redirect('/login')

    submitForm = request.form
    uid = submitForm.get("id")
    if uid != '':
        uid = int(uid)
    date = submitForm.get("date")
    regex = re.compile('^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$')
    if not regex.match(date):
        return redirect('/user/' + current_user)
    username = submitForm.get("username")
    if username != current_user:
        return redirect('/login')
    words = submitForm.get("words")
    sqlType = int(submitForm.get("sqlType")) # 0提交 / 1修改
    sql = ''''''
    if sqlType == 0:
        print(sqlType)
        sql = '''
            INSERT INTO words_table (
                date,
                username,
                words
            ) VALUES (
                "%s",
                "%s",
                "%s"
            )''' % (date, current_user, words)
    elif sqlType == 1:
        print(sqlType)
        sql = '''
            UPDATE words_table SET date="%s",
                words="%s" WHERE id="%d";
        ''' % (date, words, uid)

    sqlOperation(sql)

    return redirect('/user/' + current_user)

@app.route('/delete', methods=['POST'])
def delete():
    current_user = session.get('user_info')
    if current_user is None:
        return jsonify({
            'status': 'fail'
        })
    uid = request.form.get('id')
    if uid is not None:
        uid = int(uid)
    print(uid)
    sql = '''
        DELETE FROM words_table WHERE
            id="%d" and username="%s"
    ''' % (uid, current_user)

    sqlOperation(sql)

    return jsonify({
        'status': 'success'
    })

@app.route('/wall', methods=['GET'])
def wall():
    return render_template('wall.html')
@app.route('/fetch')
def fetch():
    date = request.args['date']
    result = []
    ret = []
    sql = '''
        SELECT (words) FROM words_table WHERE (
            date="%s"
        );
    ''' % date
    try:
        result = list(sqlRead(sql))
    except Exception:
        print('不存在！')
        result = []
    for item in result:
        ret.append({
            'words': item[0]
        })
    # print(ret)

    return jsonify({
        'fetch_list': ret
    })

if __name__ == '__main__':
    app.debug = True
    from routes.define_socket import chat_socketio
    from routes.main_route import main as main_blueprint

    app.register_blueprint(main_blueprint)
    chat_socketio.init_app(app)
    from routes import events

    chat_socketio.run(app, host='0.0.0.0', port='5000')
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # WebSocketIO报错处理：https://blog.csdn.net/xiru9972/article/details/125127955
