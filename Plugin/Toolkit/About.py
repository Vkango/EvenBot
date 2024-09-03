from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
Api=EvenBotAPI()
class About(PluginInterface):
    def getDesc(self):
        return "关于"
    def getText(self):
        return "aboutevenbot"
    def perform_action(self,data):
        Api.SendGroupMsg(data['group_id'],"EvenBot😋Ver 0.1(m) build -1")
        