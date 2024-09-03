from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
import time
Api=EvenBotAPI()
class Threadlist(PluginInterface):
    def getDesc(self):
        return "获取当前运行的任务列表"
    def getText(self):
        return "threadlist"
    def perform_action(self,data):
        msg=""
        for i in data['PluginObjs'].enumActivePlugins():
            msg+=i+"\n"
        
        Api.SendGroupMsg(data['group_id'],"😋活跃插件如下：\n"+msg+"😱为了防止把我累死，我最多可以同时开5个线程。")
        