from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
import shutil
import os
Api=EvenBotAPI()

class SetAllow(PluginInterface):
    def getDesc(self):
        return "启用下载的脚本"
    def getText(self):
        return "allow "
    def perform_action(self,data):
        if not data['message'].find("😡")==-1:
            data['message']=data['message'].replace('😡','',1)
            try:
                os.remove(".\\Temp\\"+data['message'])
                Api.SendGroupMsg(data['group_id'],f"以删除圆孔脚本😎")
            except:
                Api.SendGroupMsg(data['group_id'],f"这脚本味好像不太对🤔")

            return


        if not data['from_id']==114514:#是否是主人
            Api.SendGroupMsg(data['group_id'],f"逆势我蝶😍，但在这种情况下🤔，我的脑子以进化成唯主人为天的逻辑😘。")
            return
        try:
            shutil.move(".\\Temp\\"+data['message'],'.\\Plugin\\Download\\')
            
            Api.SendGroupMsg(data['group_id'],f"脚本启用成功，以自动刷新。😋")
            return {"need_update":"true"}
        except:
            Api.SendGroupMsg(data['group_id'],f"这脚本味好像不太对🤔")
        
        
        