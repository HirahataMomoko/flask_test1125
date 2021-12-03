# FlaskからflaskをImportして、Flaskを使えるようにする。
from flask import Flask,render_template,request,redirect,session
# sqlはフラスクとは別物なので、別の行に書く。pythonが元々持っている機能を呼び出している。
import sqlite3, random

#appっていう名前でFlaskアプリを作っていくよ
app = Flask(__name__)

app.secret_key = "sunabaco"

@app.route("/")
def top():
    return "Hello World!"

@app.route("/greet/<name>")
def greet(name):
    return name + "さん、こんにちは"

@app.route("/template")
def template():
    py_name = "あき"
    return render_template("index.html",name = py_name)


# 天気の課題
# 新しい/weatherというルートを作る。
# 関数名はweather()
# templatesフォルダの中に新しくweather.htmlを作成して
# python側で変数に代入した天気を用いて、戻り値で、weather.htmlに値を渡して
# 今日の天気はOOですと表示させる

@app.route("/weather")
def weather():
    py_weather = "晴れ"
    return render_template("weather.html",html_weather=py_weather)

# --------------------DAY2--------------------

    # git add .
    # git commit -m "天気の課題まで"
    # git push origin main
    #できたひとは、「gitignore」について調べてみてください！

# 新しい/colorというルートを作る。
# 関数名はcolor()
# 戻り値で、テンプレート（color.HTML）を表示させてください
# color.htmlに 今日のラッキーカラーは00です と表示するHTML（h1）を書きましょう
# 00には、python側で作られたpy_colorという変数の値をhtml_colorに埋め込んで表示してください。
# 表示の確認ができたらコミットまでしましょう。コミットメッセージは”ラッキーカラーページ実装”
# ここまでできたらSlackにコメントお願いします！
# ここまで終わったらFlaskでsqlite3を使うにはどうすればいいか？ググってみてね！

@app.route("/color")
def color():
    # 「sqlite3でcolor.dbに接続してね」ということをconnに代入
    conn = sqlite3.connect("color.db")
    # 「sqlite3で接続したものを操作してね」ということをcに代入
    c = conn.cursor()
    # （）内のSQL文を実行してね
    c.execute("SELECT * FROM colors")
    # 実行結果を1つだけ取って参る
    # py_color = c.fetchone()
    # 実行結果を全て取って参る
    py_color = c.fetchall()
    py_color = random.choice(py_color)
    # color.dbとの接続を終了
    c.close()
    print(py_color)
    return render_template("color.html",html_color = py_color)

# --------------------DAY3--------------------
#タスク追加のページを表示
@app.route("/add", methods = ["GET"])
def add_get():
    if "user_id" in session:
        return render_template("add.html")
    else:
        return redirect("/login")
    

#入力フォームで追加したタスクをDBに登録する処理
@app.route("/add",methods = ["POST"])
def add_post():
    if "user_id" in session:
        user_id = session["user_id"]
        task = request.form.get("task")
        #DB接続
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("insert into tasks values (null,?,?)",(task,user_id))
        #DBに登録する（＝変更を加える）ので、変更内容を保存する
        conn.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect("/login")

#リストの表示
@app.route("/list")
def list(): #DBへの接続と、データをとってくるSQL文書いてね
    if "user_id" in session:
        user_id = session["user_id"]
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("select id,task from tasks where user_id = ?",(user_id,))
        task_list = []  #task_listという変数の中の配列に以下のものを入れる
        for row in c.fetchall():   
            task_list.append({"id":row[0],"task":row[1]})
        c.close()                 
        print(task_list)         
        return render_template("list.html",task_list=task_list)
    else:
        return redirect("/login")
# --------------------DAY4--------------------

#編集
@app.route("/edit/<int:id>")
def edit(id):
    if "user_id" in session:
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("select task from tasks where id = ?",(id,))
        task = c.fetchone()
        c.close()
        if task is not None:
            task = task[0] #タプルを外している
        else:
            return "タスクがないよ"
        print(task)
        item = {"id":id,"task":task}
        return render_template("edit.html",item = item)
    else:
        return redirect("/login")

#タスクの内容を編集（更新）する
@app.route("/edit",methods = ["POST"])
def edit_post():
    if "user_id" in session:
        #入力フォームのデータを取ってくる
        task_id = request.form.get("task_id")
        task = request.form.get("task")
        #データベースと接続
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("update tasks set task = ? where id = ?",(task,task_id))
        #データの更新
        conn.commit()
        c.close()
        #/listを表示
        return redirect("/list")
    else:
        return redirect("/login")

#削除
@app.route("/del/<int:id>")
def del_task(id):
    if "user_id" in session:
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
        c.execute("delete from tasks where id = ?",(id,))
        conn.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect("/login")

# --------------------DAY5--------------------

#新規登録のページを表示
@app.route("/regist", methods=["GET"])
def regist_get():
    if "user_id" in session:
        return render_template("regist.html")
    else:
        return render_template("regist.html")

#新規登録の処理
@app.route("/regist", methods=["POST"])
def regist_post():
    #入力フォームのデータを取ってくる
    name = request.form.get("user_name")
    password = request.form.get("password")
    #DB接続
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("insert into users values (null,?,?)",(name,password))
    #DBに登録する（＝変更を加える）ので、変更内容を保存する
    conn.commit()
    c.close()
    return redirect("/login")

#ログイン画面の表示
@app.route("/login",methods = ["GET"])
def login_get():
    if "user_id" in session:
        return redirect("/list")
    else:
        return render_template("login.html")

#ログイン機能の処理
@app.route("/login", methods = ["POST"])
def login_post():
    #入力フォームのデータを取ってくる
    name = request.form.get("user_name")
    password = request.form.get("password")
    #DB接続
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("select id from users where name = ? and password = ?",(name,password))
    user_id = c.fetchone()  
    c.close()
    if user_id is None:
        return render_template("login.html")
    else:
        session["user_id"] = user_id[0]
        print(user_id)
        return redirect("/list")

#ログアウト
@app.route("/logout", methods = ["GET"])
def logout():
    session.pop("user_id",None) #sessionからuser_idを取り除く
    return redirect("/login") 












#404page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404



# __name__というのは自動的に定義される変数で、現在のファイル（モジュール）名が入ります。
if __name__ == "__main__":
    #フラスクが持っているアプリを実行します
    app.run(debug=True)