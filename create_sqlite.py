import sqlite3 as sql

def create_table():
    conn = sql.connect('database.db')
    print("Opened database successfully")

    conn.execute(
        'CREATE TABLE md_user (md_name TEXT, md_username TEXT, md_password TEXT, best_score TEXT, history_score_list TEXT)')
    conn.execute('CREATE TABLE user_now_score (md_username TEXT, now_score TEXT)')
    print("Table created successfully")
    conn.close()


def insert():

    datas = [{"md_name":"刘xx","md_username":"20200101"},
             {"md_name":"常0","md_username":"20200102"}]
    with sql.connect("database.db") as con:
        cur = con.cursor()

        for data in datas:
            print(data)
            cur.execute(
                "insert into md_user (md_name, md_username, md_password, best_score, history_score_list) VALUES(?, ?, ?, ?, ?)",
                (data["md_name"], data["md_username"], "123456", "0", ""))
            cur.execute(
                        "insert into user_now_score (md_username, now_score, md_name) VALUES(?, ?, ?)",
                        (data["md_username"], "0", data["md_name"]))
            con.commit()
    print("Table created successfully")


if __name__ == '__main__':
    insert()