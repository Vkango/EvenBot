# Source: https://github.com/alexayan/garbage-classification-data
from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
import json
from fuzzywuzzy import fuzz
Api=EvenBotAPI()
def get_level(int):
    is_ok=False
    if int==1:
        is_ok=True
        return "😃可回收垃圾"
    if int==2:
        is_ok=True
        return "😱有害垃圾"
    if int==4:
        is_ok=True
        return "💧湿垃圾"
    if int==8:
        is_ok=True
        return "🏜干垃圾"
    if int==16:
        is_ok=True
        return "📦大件垃圾"
    if is_ok==False:
        return "😎我知不道"
class Garbage(PluginInterface):
    def getDesc(self):
        return "关于"
    def getText(self):#你也可以在此处放置初始化代码
        w=open("D:\EvenBot\Plugin\Toolkit\garbage.json","rb")
        global rc
        rc=json.loads(w.read())
        global r
        r=[]
        for i in range(len(rc)):
           r.append(rc[i]['name']) 
        w.close()
        return "garbage "
    def perform_action(self,data):
        msg=""
        for i in range(len(r)):
            if fuzz.ratio(data['message'],r[i])>70:
                msg+=r[i]+" | "+get_level(rc[i]['category'])+"\n"
        if msg=="":
            Api.SendGroupMsg(data['group_id'],"😭我没找到...")
            return   
        Api.SendGroupMsg(data['group_id'],"为你找到如下结果：\n"+msg+"😋垃圾分类，从俺做起！")
        