# coding=utf-8
from flask import Flask
from flask import render_template
from excel import parser
from flask import request
from flask import abort, redirect, url_for

app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit():
    print "获取到一个请求"
    year = request.form.get('year')
    if year is None:
        print "fuck"
    print year
    parser.excel(float(year))
    return render_template("world.html", year=year)


@app.route('/test')
def test():
    year = 2007
    return render_template("world.html", year=year)

if __name__ == '__main__':
    app.run()
