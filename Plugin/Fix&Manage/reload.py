from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
Api=EvenBotAPI()
def __init__():
    print("Init")
class Reload(PluginInterface):
    def getDesc(self):
        return "重载指定插件"
    def getText(self):
        return "reload "
    def perform_action(self,data):#即使不使用也必须带着data
        try:
            data['PluginObjs'].reload_plugin(data["message"])
            Api.SendGroupMsg(data['group_id'],"已重载插件："+data['message'])
        except Exception as e:
            Api.SendGroupMsg(data['group_id'],f"重载失败，{e}")
    