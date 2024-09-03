from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
Api=EvenBotAPI()
class EvenBot_USERSCRIPT_TEST(PluginInterface):
    def getText(self):
        return "evenscript"
    def perform_action(self,data):
        Api.SendGroupMsg(data['group_id'],"测试以成功。")