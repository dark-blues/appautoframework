# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : testindex.py
@desc: 
@Created on: 2020/10/20 14:04
"""
import json
import unittest
import time
import ddt
from airtest.core.api import *
from airtest.cli.parser import cli_setup
import logging
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from Base.BaseSettings import LOG_DIR, REPORT_DIR, DATA_DIR
from Base.BaseSettings import  Android1 as Android

from Base.PublicFunction import make_dir, poco_wait, report_DIYdata, render_directory
from Base.lib import simple_reports

index_log_dir = LOG_DIR+"index\\"  #D:/Pycharm/PythonProject/app29\Logs\   index\\每日推荐
index_report_dir = REPORT_DIR + "index\\"
report_data_dir = REPORT_DIR+"reportdata\\"
index_data_dir = DATA_DIR+"index\\"



@ddt.ddt
class TestIndex(unittest.TestCase):

    def setUp(self) -> None:
        # start_app("com.netease.cloudmusic")
        pass


    @classmethod
    def setUpClass(cls) -> None:
        logger = logging.getLogger("airtest")
        logger.setLevel(logging.ERROR)

        if not cli_setup():
            only_auto_setup(__file__,  devices=[
                Android,
            ])

        start_app("com.netease.cloudmusic")
        cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

    def tearDown(self) -> None:
        # stop_app("com.netease.cloudmusic")
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        # stop_app("com.netease.cloudmusic")
        pass


    @ddt.file_data(index_data_dir+"c.yaml")
    def testbanner(self,**kwargs):
        test_result= True
        start_time= time.time()
        case_log_dir=index_log_dir+kwargs.get("casename")
        make_dir(case_log_dir)
        set_log_dir(__file__,case_log_dir)

        try:
            # 点击对应 case
            self.poco(text=kwargs.get("casename")).click()
            if kwargs.get("casename")=="每日推荐":
                day = self.poco("com.netease.cloudmusic:id/dayRecommendDateInfo").attr("text")

                real_day = time.strftime('%d', time.localtime(time.time()))
                print(day, real_day)
                assert_equal(day, real_day, "时间是否正确")

                all_button = self.poco("com.netease.cloudmusic:id/playAllTextView").exists()
                assert_equal(all_button, True, "播放全部按钮是否存在")

                song_name = \
                self.poco("android.widget.LinearLayout").offspring("com.netease.cloudmusic:id/pagerListview").child("com.netease.cloudmusic:id/musicListItemContainer")[0].offspring("com.netease.cloudmusic:id/songInfoContainer").child("com.netease.cloudmusic:id/songInfo").attr("text")
                print(song_name)
                self.poco(text=song_name).click()
                assert_exists(Template(index_data_dir+"tpl1603158907858.png", record_pos=(0.002, 0.95), resolution=(1080, 2340)), "成功播放")
                assert_equal(self.poco(text=song_name).exists(), True, "歌名与点击的一致")
                keyevent("BACK")
            else:
                assert_exists(Template(index_data_dir+kwargs.get("picture"), record_pos=eval(kwargs.get("record_pos")), resolution=(1080, 2340)), kwargs.get("assert_info"))

            # keyevent("BACK")
        except Exception as e:
            log(e,desc="Error:报错信息")
            test_result =False
        finally:
            while True:
                res = self.poco(text="每日推荐").exists() and self.poco(text="私人FM").exists()
                if  not res:
                    foucekeyevent("BACK")
                    time.sleep(0.5)
                else:
                    break

            from airtest.report.report import simple_report
            # simple_report(__file__, logpath=case_log_dir,output=index_report_dir+kwargs.get("casename")+".html")
            simple_reports(__file__, logpath=case_log_dir,output=index_report_dir+kwargs.get("casename")+".html",kwargs=kwargs)
            html_path = index_report_dir + kwargs.get("casename") + ".html"
            report_DIYdata(kwargs,start_time,html_path,"zs",__file__,test_result)

    @unittest.skip
    def testsearh(self):
        case_log_dir = index_log_dir + "搜索"
        make_dir(case_log_dir)
        set_log_dir(__file__, case_log_dir)

        try:
            self.poco("搜索").click()
            text("沉默是金")
            poco_wait(self.poco,"text","张国荣 - Ultimate ")
            assert_equal(self.poco(text="张国荣 - Ultimate ").exists(),True,"该元素存在")
            self.poco(text="张国荣 - Ultimate ").click()
            assert_exists(Template(index_data_dir+"tpl1603158907858.png", record_pos=(0.002, 0.95), resolution=(1080, 2340)), "成功播放")
            res = exists(Template(index_data_dir+"tpl1603175359480.png", record_pos=(-0.352, 0.696), resolution=(1080, 2340),threshold=0.85))
            if not res:
                self.poco("com.netease.cloudmusic:id/likeBtn").click()
            keyevent("BACK")
            keyevent("BACK")
            keyevent("BACK")
            self.poco(name = "我的音乐").click()
            self.poco("com.netease.cloudmusic:id/name").click()
            assert_equal(self.poco(text="张国荣 - Ultimate ").exists(), True, "是否加入收藏")
            keyevent("BACK")
            self.poco("搜索").click()
            time.sleep(1.5)
            assert_equal(self.poco(text="沉默是金").exists(), True, "是否有搜索历史")
            self.poco("com.netease.cloudmusic:id/cancel").click()
            self.poco("com.netease.cloudmusic:id/buttonDefaultPositive").click()
            time.sleep(1.5)
            assert_equal(self.poco(text="历史").exists(), False, "是否清空搜索历史")
        except Exception as e:
            print(e)

        finally:
            from airtest.report.report import simple_report
            simple_reports(__file__, logpath=case_log_dir,output=index_report_dir+"搜素.html")


if __name__ == '__main__':
    unittest.main()
