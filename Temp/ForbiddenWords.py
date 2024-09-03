from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
import time
import html
Api=EvenBotAPI()
class ForbiddenWords(PluginInterface):
    def getDesc(self):
        return "违禁词"
    def getText(self):
        return ""
    def perform_action(self,data):
        if(data['message']=="baideng"):
            Api.SendGroupMsg(data['group_id'],"请规范发言，否则我们将向您的电脑内植入圆孔。")
        