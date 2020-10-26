# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : lib.py
@desc: 
@Created on: 2020/10/25 17:00
"""
import json
import os

from airtest.cli.info import get_script_info
from airtest.report.report import LogToHtml
from airtest.utils.compat import script_dir_name

from Base.BaseSettings import ipport, static_dir


class DIYLogToHtml(LogToHtml):

    def DIY_report_data(self, output_file=None, record_list=None,kwargs={}):
        """
        Generate data for the report page
        :param output_file: The file name or full path of the output file, default HTML_FILE
        :param record_list: List of screen recording files
        :return:
        """
        self._load()
        # steps 列表  存放的是 """ 解析log成可渲染的dict """
        steps = self._analyse()

        script_path = os.path.join(self.script_root, self.script_name)  # __file__  运行脚本的路径

        ## script_name  当前运行脚本的文件名
        # script_path  当前运行脚本的文件路径
        # author, title, desc  当前运行脚本内的__author, title, desc__信息  没有就是空
        # {"name": script_name, "path": script_path, "author": author, "title": title, "desc": desc}
        info = json.loads(get_script_info(script_path))
        info["author"] = kwargs.get("casecreate")
        info["title"] = kwargs.get("casename")
        info["desc"] = kwargs.get("casedesc")
        # []

        records = [os.path.join("log", f) if self.export_dir
                   else os.path.abspath(os.path.join(self.log_root, f)) for f in record_list]

        if not self.static_root.endswith(os.path.sep):
            self.static_root = self.static_root.replace("\\", "/")
            self.static_root += "/"

        data = {}
        data['steps'] = steps
        data['name'] = self.script_root
        data['scale'] = self.scale
        data['test_result'] = self.test_result
        data['run_end'] = self.run_end
        data['run_start'] = self.run_start
        data['static_root'] = self.static_root
        data['lang'] = self.lang
        data['records'] = records  # []
        data['info'] = info
        data['log'] = self.get_relative_log(output_file)
        data['console'] = self.get_console(output_file)
        # 如果带有<>符号，容易被highlight.js认为是特殊语法，有可能导致页面显示异常，尝试替换成不常用的{}
        info = json.dumps(data).replace("<", "{").replace(">", "}")  # info 字符串  data 数据 字典转的字符串
        info = info.replace("\\\\","\\")
        # data['data'] = info.replace("D:\\Pycharm\\PythonProject\\app29\\entrance\\static","http://10.10.10.172:5000/static")
        data['data'] = info.replace(static_dir, ipport + "static")  #D:\\Pycharm\\PythonProject\\app29\\entrance\\static
        print(data['data'] )
        return data

    def DIYreport(self, template_name="log_template.html", output_file=None, record_list=None,kwargs={}):
        """
        Generate the report page, you can add custom data and overload it if needed
        :param template_name: default is HTML_TPL  #"log_template.html"
        :param output_file: The file name or full path of the output file, default HTML_FILE
        :param record_list: List of screen recording files
        :return:
        """
        if not self.script_name:
            path, self.script_name = script_dir_name(self.script_root)

        if self.export_dir:
            self.script_root, self.log_root = self._make_export_dir()
            # output_file可传入文件名，或绝对路径
            output_file = output_file if output_file and os.path.isabs(output_file) \
                else os.path.join(self.script_root, output_file or "log.html")
            if not self.static_root.startswith("http"):
                self.static_root = "static/"

        if not record_list:
            record_list = [f for f in os.listdir(self.log_root) if f.endswith(".mp4")]  # []
        data = self.DIY_report_data(output_file=output_file, record_list=record_list,kwargs=kwargs)
        return self._render(template_name, output_file, **data)



def simple_reports(filepath, logpath=True, logfile="log.txt", output="log.html",kwargs={}):
    path, name = script_dir_name(filepath)
    if logpath is True:
        logpath = os.path.join(path, "log")
    rpt = DIYLogToHtml(path, logpath, logfile=logfile, script_name=name,static_root=ipport+"static",lang="zh")
    rpt.DIYreport("log_template.html", output_file=output,kwargs=kwargs)