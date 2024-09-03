# 百度汉语API，客户端抓包
# 侵删。
import json
import urllib.parse
from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
import requests
import urllib
Api=EvenBotAPI()
class bdhanyu(PluginInterface):
    def getDesc(self):
        return "查字、查词"
    def getText(self):
        return "hanyu "
    def perform_action(self,data):
        #很奇怪の写法~
        url="https://hanyuapp.baidu.com/dictapp/v3/s?wd="+urllib.parse.quote(data['message'])
        x=requests.get(url)
        jsonObj=json.loads(x.text)
        msg=""
        msg+="Source: hanyu.baidu.com\n【"+data['message']+"】"
        for means in range(len(jsonObj['data']['ret_array'][0]["mean_list"])):
            #pin_yin
            print(jsonObj['data'])
            for i in range(len(jsonObj['data']['ret_array'][0]["mean_list"][means]['pinyin'])):
                msg+="("+jsonObj['data']['ret_array'][0]["mean_list"][means]['pinyin'][i]+")"
            msg+="\n"
            for i in range(len(jsonObj['data']['ret_array'][0]["mean_list"][means]['definition'])):
                msg+="{0}. ".format(i+1)+jsonObj['data']['ret_array'][0]["mean_list"][means]['definition'][i]+"\n"
            msg+="没了。"
        Api.SendGroupMsg(data['group_id'],msg)