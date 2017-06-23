# coding=utf-8
from flask import Flask
from flask import render_template
from excel import parser
from flask import request
import os
import time
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, patch_request_class

app = Flask(__name__)
# 文件储存地址
path = os.getcwd() + os.path.sep + 'static' + os.path.sep + 'data'
app.config['UPLOADED_FILES_DEST'] = path
print("path:", path)

files = UploadSet('files', DOCUMENTS)
configure_uploads(app, files)
patch_request_class(app)


@app.route('/lines')
def hello_world():
    return render_template("echart/lines.html")


@app.route('/')
def index():
    return render_template("center.html")


@app.route('/submit', methods=['POST'])
def submit():
    print ("获取到一个请求")
    filename = files.save(request.files['file'], 'excel', 'file-' + str(time.time()) + '.xlsx')
    print("上传了文件：", filename)
    # file_url = files.url(filename)
    # print(file_url)
    year = request.form.get('year')
    start = int(request.form.get('start'))
    end = int(request.form.get('end'))
    if year is None:
        print("fuck")
    print("year=", year)
    print("start=", start)
    print("end=", end)

    parser.parseStartAndEnd(float(year), start, end)
    return render_template("echart/lines.html", year=year)


@app.route('/test')
def test():
    year = 2007
    return render_template("world.html", year=year)

if __name__ == '__main__':
    app.run()
