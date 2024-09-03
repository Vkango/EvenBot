from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
import os
Api=EvenBotAPI()
class Menu(PluginInterface):
    def getDesc(self):
        return "菜单"
    def getText(self):
        return "evenMenu"
    def perform_action(self,data):
        Api.SendGroupMsg(data['group_id'],"[CQ:image,file=D:\EvenBot\Plugin\Toolkit\Menu.png]")
        