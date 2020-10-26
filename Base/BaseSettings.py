# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : BaseSettings.py
@desc: 
@Created on: 2020/10/20 11:53
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

entrance_dir = os.path.join(BASE_DIR,"entrance\\")
static_dir=os.path.join(entrance_dir,"static\\")
LOG_DIR = os.path.join(static_dir,"Logs\\")
REPORT_DIR = os.path.join(entrance_dir,"static\\Report\\")
DATA_DIR = os.path.join(static_dir,"TestData\\")
report_data_dir = os.path.join(REPORT_DIR,"reportdata\\")
USERNAME = "zs"
PD = "123456"
ipport = "http://10.10.10.172:5000/"
result_html = os.path.join(static_dir,"result.html")

Android1 = "Android://127.0.0.1:5037/954f932f"

if __name__ == '__main__':
    print(__file__)
    print(os.path.basename(__file__))
    print(static_dir)