# ps吧热帖查看
# API以及SIGN算法均来自网络，非原创！
# 侵删。
from urllib.parse import unquote
from urllib.parse import quote
import requests
import hashlib
import json
import random
from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
Api=EvenBotAPI()
def CalcSign(Original_Data):#计算sign
    text=Original_Data
    proceed=unquote(text)
    proceed=proceed.replace("&","",-1)+"tiebaclient!!!"
    proceed=hashlib.md5(proceed.encode()).hexdigest()
    return text+"&sign="+proceed.upper()
def BrowseBar(Bar_Name):
    # 先找热帖
    r=requests.post("http://c.tieba.baidu.com/c/f/frs/page",data=CalcSign("_client_type=2&_client_version=8.6.8.0&kw="+quote(Bar_Name)+"&pn=2&q_type=2&rn=50&with_group=1"))
    Threads=json.loads(r.text)
    r.close()
    threadsi={}
    like_info=[]
    result={}
    for i in range(len(Threads["thread_list"])):
        if(Threads['thread_list'][i]['reply_num']<120):# 回复数量<120的我不要
            continue
        threadsi[Threads['thread_list'][i]['reply_num']]=Threads['thread_list'][i]['id']
        like_info.append(Threads['thread_list'][i]['reply_num'])# 加入列表({回复数量:贴子ID})
    like_info.sort(reverse=True)#反向排序
    if(len(like_info)==0):
        result['ok']=False#用于下面的，现在还没有热帖哦~
        return result
    result['ok']=True#现在有热帖哦~
    result['id']=str(threadsi[random.choice(like_info)])#热帖ID
    # 浏览贴子
    r=requests.post("http://c.tieba.baidu.com/c/f/pb/page",CalcSign("_client_version=7.2.2&kz="+result['id']+"&net_type=1&pn=1"))
    Post=json.loads(r.text)
    r.close()
    result['title']=Post['thread']['title']
    result['img_1']=""#楼主发了什么图
    result['img_2']=""#回复者发了什么图
    for i in range(len(Post['post_list'][0]['content'])):
        if(Post['post_list'][0]['content'][i]['type']==3):#只要图片
            result['img_1']=Post['post_list'][0]['content'][i]['origin_src']
            break
    for i in range(len(Post['post_list'])-1):
        i+=1
        for ic in range(len(Post['post_list'][i]['content'])):
            if(Post['post_list'][i]['content'][ic]['type']==3):
                result['img_2']=Post['post_list'][i]['content'][ic]['origin_src']
                break
        if not result['img_2']=="":
            break
    return result
class ps_bar_post(PluginInterface):
    def getText(self):
        return "can can ps bar"
    def perform_action(self,data):
        res=BrowseBar("ps")
        if not res['ok']:
            Api.SendGroupMsg(data['group_id'],"😱现在还没有热帖嗷~")
            return
        Api.SendGroupMsg(data['group_id'],f"🔗https://tieba.baidu.com/p/{res['id']}"+"\n📄"+res['title']+"\n"+f"[CQ:image,file={res['img_1']}]"+"\n👉RE:\n"+f"[CQ:image,file={res['img_2']}]")