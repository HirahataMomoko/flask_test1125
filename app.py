# FlaskからflaskをImportして、Flaskを使えるようにする。
from flask import Flask,render_template

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






# __name__というのは自動的に定義される変数で、現在のファイル（モジュール）名が入ります。
if __name__ == "__main__":
    #フラスクが持っているアプリを実行します
    app.run(debug=True)