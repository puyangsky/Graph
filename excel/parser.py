# -*- coding:utf-8 -*-
from __future__ import print_function
import json
import xlrd
import os
import util
# reload(sys)
# sys.setdefaultencoding('utf-8')
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class Model(json.JSONEncoder):
    def __init__(self, code, z):
        super(Model, self).__init__()
        self.code = code
        self.z = z

    def default(self, obj):
        if isinstance(obj, Model):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)

    def to_dict(self):
        return {"code": self.code, "z": self.z}


class Flow(json.JSONEncoder):

    def __init__(self, start, end, weight):
        self.start = start
        self.end = end
        self.weight = weight

    def default(self, obj):
        if isinstance(obj, Model):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)

    def to_dict(self):
        return {"start": self.start, "end": self.end, "weight": self.weight}


def func1(dir_name=None):
    f = open(dir_name + "code_map.txt", "r")
    m = {}
    for l in f.readlines():
        # print l
        l = l.strip("\n")
        ls = l.split("\t")
        m[ls[1]] = ls[0]
        # print ls[0] + "\t" + ls[1]
    return m


def excel(year):
    if year is None:
        year = 2007.0
    else:
        year = float(year)
    dir_name = os.getcwd() + os.path.sep + 'static' + os.path.sep + 'data' + os.path.sep
    # print dir_name
    data = xlrd.open_workbook(dir_name + 'excel.xlsx')
    # print data
    table = data.sheets()[0]

    nrows = table.nrows

    m = func1(dir_name)
    mm = []
    for i in range(nrows):
        row = table.row_values(i)
        if row[0] != year:
            continue
        k = row[1].encode("utf-8")
        if k in m.keys():
            print(m[k], "\t", row[4])
            model = Model(m[k], row[4])
            # 只有__dict__对象才能进行json序列化
            mm.append(model.__dict__)
        else:
            eprint("[WARN] No map, kye: " + k)

    json.dump(mm, open(dir_name + str(int(year)) + ".json", 'w'))
    print("[INFO] Done!")


# 解析StartAndEnd.xlsx
def parseStartAndEnd(year=None, startIndex=0, endIndex=0):
    if year is None:
        year = 2007.0
    else:
        year = float(year)
    dir_name = '/Users/imac/PycharmProjects/Graph/static/data/'
    data = xlrd.open_workbook(dir_name + 'StartAndEnd.xlsx')
    table = data.sheets()[0]

    nrows = table.nrows
    if nrows < endIndex or startIndex < 1:
        eprint("下标输入错误，越界")
        return
    column = 0
    jsonArray = []
    for i in range(startIndex-2, endIndex):
        row = table.row_values(i)
        if i == 1:
            for j in range(len(row)):
                if row[j] == year:
                    column = j
        else:
            startCountry = row[0]
            endCountry = row[1]
            if '*' in startCountry or '*' in endCountry:
                continue
            if u'其他国家' == endCountry or u'世界' == endCountry:
                continue
            print(startCountry, endCountry, row[column])
            flow = Flow(row[0], row[1], row[column])
            jsonArray.append(flow.__dict__)
    json.dump(jsonArray, open(dir_name + "StartAndEnd-" + str(int(year)) + ".json", 'w'))

if __name__ == '__main__':
    parseStartAndEnd(2007.0, 3, 23)
