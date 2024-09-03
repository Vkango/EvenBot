from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
import html # 转编码用
Api=EvenBotAPI()
def GetClassName(str):#内部文本处理，用来获取Class名
    try:
        loc1=str.find("class ")
        loc2=str.find("(PluginInterface):")
        return str[loc1+len("class "):loc2]
    except:
        return ""
class DownloadScript(PluginInterface):
    def getDesc(self):
        return "下载脚本"
    def getText(self):
        return "download "
    def perform_action(self,data):
        classname= GetClassName(data['message'])
        if(classname==""):#不下载空脚本
            Api.SendGroupMsg(data['group_id'],f"这脚本味好像不太对🤔")
            return
        mana=data['PluginData']
        for names in mana:
            if(names[0]==classname):#class名冲突 TODO:利用互动消息做更换Class名操作
                Api.SendGroupMsg(data['group_id'],f"换个Class名吧😋")
                return
        # 写出脚本
        if not data['from_id']==114514:# 如果不是管理员
            # 写入Temp目录而不是Plugin目录，防止下一次重载时载入造成安全隐患
            with open(".\\Temp\\"+classname+".py","w",encoding="utf-8") as f:
                f.write(html.unescape(data['message']))
                f.close()
            f.close()
            Api.SendGroupMsg(data['group_id'],f"脚本下载成功，但已默认禁用，请管理员使用allow允许。\nfile："+classname+".py")
            return
        # 如果是管理员，则可以直接下载到Plugin\Download目录，下次重载即可自动启动使用
        with open(".\\Plugin\\Download\\"+classname+".py","w",encoding="utf-8") as f:
            f.write(html.unescape(data['message']))
            f.close()
        f.close()
        Api.SendGroupMsg(data['group_id'],f"脚本下载成功，已自动刷新。")
        return {"need_update":"true"}
        # TODO: 1.使用互动消息将downloadScript.py和SetAllow.py进行联动，即成员发送消息并at管理员审核，管理员发送allow即可自动允许对应脚本运行。
        # TODO: 2.need_update属性暂时不可用，仍需要发送upd手动刷新
        #       需要在EvenBot_API中加入对EvenBot_Core、EvenBot_Plugin_Core的控制
        