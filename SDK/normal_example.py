from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
Api=EvenBotAPI()
class YourPlugin(PluginInterface):
    def getDesc(self):
        return "SDK示例，注意把YourPlugin更改！"
    def getText(self):
        return "此处写机器人触发词！"
    def perform_action(self,data):
        # 请仔细查看data中包含了什么数据，另外，message已去掉触发词。
        return "114514"