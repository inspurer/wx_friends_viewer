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
        for key,value in dic_city.items():
            print(key,value)
        # city的可视化过程类似province

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

if __name__ =="__main__":
    wechat_friends_viewer().run()
