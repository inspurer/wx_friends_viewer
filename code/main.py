# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_date:      2019/1/24
# file_name:        main.py
# github            https://github.com/inspurer
# qq_mail           2391527690@qq.com

import itchat
import json
import os
import re
from pyecharts import Geo

class wechat_friends_viewer():
    def __init__(self):
        # 弹出扫码登录界面,参数这样设置的好处是短时间内退出程序，再次登录可以不用扫码
        itchat.auto_login(hotReload=True)

        self.friends = itchat.get_friends(update=True)

        # print(self.friends,type(self.friends),len(self.friends))
        # 把json对象转成字符串并保存在本地
        with open("data.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.friends, indent=2, ensure_ascii=False))

    def sex_viewer(self):
        unknow = male = female = 0
        for friend in self.friends:
            if friend["Sex"] == 0:
                unknow += 1
            elif friend["Sex"] == 1:
                male += 1
            else:
                female +=1
        print(unknow,male,female)
        view_sex = ""
        with open("view/sex.html","r",encoding="utf-8") as f:
            view_sex = f.read()
        view_sex = view_sex.replace("value:24","value:"+str(unknow))
        view_sex = view_sex.replace("value:92","value:"+str(male))
        view_sex = view_sex.replace("value:40","value:"+str(female))
        with open("view/your_sex.html","w",encoding="utf-8") as f:
            f.write(view_sex)
        os.startfile(os.getcwd()+"/view/your_sex.html")

    def province_viewer(self):
        dic_province = dict()
        for friend in self.friends:
            key = friend["Province"]
            if key not in dic_province.keys():
                dic_province[key] = 1
            else:
                dic_province[key] += 1
        key_list = []
        value_list = []
        for key,value in dic_province.items():
            if key == "":
                key = "其他地区"
            key_list.append(key)
            value_list.append(value)
        print(json.dumps(key_list,ensure_ascii=False))
        print(json.dumps(value_list,ensure_ascii=False))
        view_province = ""
        with open("view/province.html","r",encoding="utf-8") as f:
            view_province = f.read()
        view_province = view_province.replace('["湖南"]',json.dumps(key_list,ensure_ascii=False))
        view_province = view_province.replace('[50]',json.dumps(value_list,ensure_ascii=False))
        with open("view/your_province.html","w",encoding="utf-8") as f:
            f.write(view_province)
        os.startfile(os.getcwd()+"/view/your_province.html")


    def city_viewer(self):
        dic_city = dict()
        for friend in self.friends:
            key = friend["City"]
            if key not in dic_city.keys():
                dic_city[key] = 1
            else:
                dic_city[key] += 1

        data = []
        max_value = 0
        for key,value in dic_city.items():
            # 其他地区
            if len(key) == 0:
                continue
            # 过滤英文等非市级
            if len(key) >= 3:
                continue

            # 没有找到判断字符串是不是城市的接口，暂时先这样过滤吧
            if key == "海淀" or key == "南开" or key == "徐汇":
                continue
            data.append(tuple((key,value)))
            if value > max_value:
                max_value = value
            print(key,value)
        print(data)
        # city的可视化过程类似province
        ## 高级可视化
        # 安装 pyecharts
        # pip install  pyecharts
        # 安装 独立的地图包
        # pip install echarts-countries-pypkg
        # pip install echarts-china-provinces-pypkg
        # pip install echarts-china-cities-pypkg
        # may need pip install pyecharts_snapshot

        geo = Geo("微信好友城市分布图", "posted by inspurer", title_color="#000",
                  title_pos="center", width=1000,
                  height=600, background_color='#ffffff')
        attr, value = geo.cast(data)
        geo.add("", attr, value, visual_range=[1, max_value], visual_range_color=['#d54d2b', '#FF0000'],
                maptype='china', visual_text_color="#f00",
                symbol_size=18, is_visualmap=True,geo_normal_color="#22DDDD",geo_emphasis_color="#0033FF")
        geo.render("view/your_city.html")  # 生成html文件
        os.startfile(os.getcwd() + "/view/your_city.html")


    def sign_wordcloud(self):
        all_sign = ""
        for friend in self.friends:
            sign = friend["Signature"]
            if len(sign)>0:
                # 过滤表情，否则会对词云造成影响
                emoji = re.findall("<span class=.*></span>",sign,re.S)
                if len(emoji) > 0:
                    sign = sign.replace(emoji[0],"")
                all_sign = all_sign + sign + "\n"
        if os.path.exists("wc/sign.txt"):
            os.remove("wc/sign.txt")
        with open("wc/sign.txt","a+",encoding="utf-8") as f:
            f.write(all_sign)


    def run(self):
        self.province_viewer()
        self.sex_viewer()
        self.sign_wordcloud()
        self.city_viewer()

if __name__ =="__main__":
    wechat_friends_viewer().run()
