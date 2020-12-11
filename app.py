from flask import render_template, jsonify
from flask import request
from flask import Flask, session, redirect, url_for
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'md_pw'
DATABASE = 'database.db'


@app.route('/')
def index():
    if 'md_username' in session:
        md_username = session['md_username']
        md_name = session['md_name']
        return render_template('index.html', login_status='/logout', login_control='注销', md_username=md_username, md_name=md_name)
    return render_template('index.html', login_status='/login', login_control='登录')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login_action', methods=["post"])
def login_action():
    if 'md_username' in session:
        md_username = session['md_username']
        md_name = session['md_name']
        return render_template('index.html', login_status='/logout', md_username=md_username, md_name=md_name)
    login_message = request.form
    md_username = login_message['md_username']
    md_password = login_message['md_password']
    print(md_username, md_password, type(md_username), type(md_password))

    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from md_user where md_username=" + md_username)
    rows = cur.fetchall();
    print(rows, rows[0]['md_username'], len(rows))
    print(type(rows), type(rows[0]))
    if len(rows) > 0 and md_username == rows[0]['md_username']:
        if md_password == rows[0]['md_password']:
            session['md_username'] = md_username
            session['md_name'] = rows[0]['md_name']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', resulte_message='密码错误')
    else:
        return render_template('login.html', resulte_message='未找到该账号')


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('md_username', None)
    session.pop('md_name', None)
    return redirect(url_for('index'))


@app.route('/up_score', methods=['POST'])
def up_score():
    try:
        md_username = session['md_username']
        now_score = request.form['now_score']
        print(md_username, now_score)

        with sql.connect("database.db") as con:
            cur = con.cursor()
            # cur.execute("UPDATE user_now_score SET now_score = '5' WHERE md_username = 20206666")
            cur.execute("update user_now_score set now_score=" + now_score + " WHERE md_username=" + md_username)
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
    finally:
        return jsonify({'code': 200, 'message': ''})


@app.route('/register')
def register():
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()

            cur.execute("insert into md_user (md_name, md_username, md_password, best_score, history_score_list) VALUES(?, ?, ?, ?, ?)",("彭1", "20201111", "123456", "9999", "1,23,777,9999"))
            cur.execute(
                "insert into user_now_score (md_username, now_score, md_name) VALUES(?, ?, ?)",
                ("20201111", "0", "彭2"))
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"

    finally:
        return render_template("index.html")


@app.route('/get_top_list', methods=['POST'])
def get_top_list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from user_now_score")

    rows = cur.fetchall();

    result_data = []
    for row in rows:
        one_data = {"md_name": row["md_name"], "md_username": row["md_username"], "md_score": row["now_score"]}
        # print(one_data)
        result_data.append(one_data)
    print(result_data)
    result_data.sort(key=lambda k: (k.get('md_score', 0)), reverse=True)

    return jsonify({'code': 200, 'message': result_data})


@app.route('/history')
def history():
    return render_template("history.html")


@app.route('/bestone')
def bestone():
    return render_template("bestone.html")


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8080) 
