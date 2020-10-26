# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : PublicFunction.py
@desc: 
@Created on: 2020/10/20 11:53
"""
import json
import os
import shutil
import time

import jinja2
from airtest.core.error import TargetNotFoundError

from Base.BaseSettings import report_data_dir, BASE_DIR, ipport, result_html, entrance_dir


def make_dir(filepath):
    if os.path.exists(filepath):
        shutil.rmtree(filepath)
    os.mkdir(filepath)

def poco_wait(poco,fangfa,ele,timeout=10,interval=0.5):
    start_time = time.time()
    while True:
        if fangfa == "text":
            res = poco(text=ele).exists()
        else:
            res = poco(ele).exists()
        if res:
            break
        else:
            if (time.time() - start_time) > timeout:
                raise TargetNotFoundError('Picture %s not found in screen')
            else:
                time.sleep(interval)

def report_DIYdata(kwargs,start_time,html_path,author,file_path,test_result):
    case_data = {}
    # D:\Pycharm\PythonProject\app29\entrance\static\Report\index\排行榜.html
    # D:\Pycharm\PythonProject\app29\entrance\      "http://10.10.10.172:5000/"  \static\Report\index\排行榜.html
    case_data['html_path'] = html_path.replace(entrance_dir,ipport)
    print(case_data['html_path'])
    case_data['case_zh'] = kwargs.get("casename")
    case_data['case_create'] = kwargs.get("casecreate")
    case_data['author'] = author
    case_data['case_desc'] = kwargs.get("casedesc")
    case_data['file_path'] = file_path
    case_data['run_time'] = round(time.time() - start_time, 1)
    case_data['test_result'] = test_result
    case_data['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    case_info = json.dumps(case_data)
    txtpath = report_data_dir + kwargs.get("casename") + ".txt"
    with open(txtpath, "w", encoding="utf-8") as f:
        f.write(case_info)

def render_directory():
    """ 用jinja2渲染html"""
    # template_name "log_template.html
    # output_file  html输出地址
    # template_vars  kwags
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(BASE_DIR),
        extensions=(),
        autoescape=True
    )
    report_data_list = []
    template = env.get_template("Template.html")
    report_data_list_filename = os.listdir(report_data_dir)
    # print(report_data_list_filename)
    i = 0
    sum_time = 0
    for report_data_filename in report_data_list_filename:
        with open(report_data_dir+report_data_filename,"r") as f:
            report_data = json.loads(f.read())
            if report_data['test_result'] is True:
                i+=1
            sum_time += report_data['run_time']
            report_data_list.append(report_data)
    detail_info ={}
    detail_info['sum'] = len(report_data_list)
    detail_info['success_num'] = i
    detail_info['error_num'] = detail_info['sum'] -detail_info['success_num']
    detail_info['percent'] = str(round(detail_info['success_num']/detail_info['sum'],4)*100)+"%"
    detail_info['sum_time'] = sum_time
    html = template.render(report_data_list=report_data_list,detail_info=detail_info)


    with open(result_html, 'w', encoding="utf-8") as f:
        f.write(html)

if __name__ == '__main__':
    # filename = r"D:\Pycharm\PythonProject\app29\Logs\index\每日推荐log"
    # make_dir(filename)
    render_directory()