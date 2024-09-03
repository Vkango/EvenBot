from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
import time
Api=EvenBotAPI()
InteractData={}
class Music_Heng(PluginInterface):
    def getDesc(self):
        return "哼唱识别"
    def getText(self):
        return "heng"
    def perform_action(self,data):
        Api.SendGroupMsg(data['group_id'],"好的，请唱🎤，我在听👂，若不回复语音消息，将自动退出功能。")
        USER_DATA={}
        USER_DATA['Step']=0
        InteractData[data['group_id']+data['from_id']]=USER_DATA
        return {"need_interact":True,"group_id":data['group_id'],"from_id":data['from_id']}# 此处提醒Plugin_Core此群此用户已进入互动模式！并传入用户数据！
        # 使用InteractData存储对话信息，Key为群号+QQ号，对应的数据为在这一步储存的数据！~
    def perform_action_interact(self,data):
        # 开始前请务必核实消息来源，是否为同一个群下同一个人，避免数据发生冲突！
        # 此处data数据和perforom_action数据一致
        # 你可以在InteractData中存储数据，比如用户进展到了第几步之类的~
        # 执行到最后一步时，务必清除InteractData中的成员，以免造成冲突！

        # 实例：定位User
        USER_DATA=InteractData[data['group_id']+data['from_id']]
        if data['message']=="exit":
            del InteractData[data['group_id']+data['from_id']]
            Api.SendGroupMsg(data['group_id'],"😋以退出互动。")
            return {'need_interact': False,"group_id":data['group_id'],"from_id":data['from_id']} 
        if USER_DATA['Step']==0:
            if data['message'].find("[CQ:record,file=")==-1:#退出识别。
                del InteractData[data['group_id']+data['from_id']]
                #Api.SendGroupMsg(data['group_id'],"😋以退出互动。")
                # 静默退出
                return {'need_interact': False,"group_id":data['group_id'],"from_id":data['from_id']} 
            Api.SendGroupMsg(data['group_id'],"😋稍候，识别中……")
            time.sleep(5)
            Api.SendGroupMsg(data['group_id'],"😭识别失败，但您的美音以被我记录在案😈。")
        

        # 别忘了加一步！~
        USER_DATA['Step']+=1
        # 覆写全局变量
        InteractData[data['group_id']+data['from_id']]=USER_DATA
        return {'need_interact': False,"group_id":data['group_id'],"from_id":data['from_id']} if USER_DATA['Step'] == 1 else {"need_interaction":True,"group_id":data['group_id'],"from_id":data['from_id']}
        # 注意：此处need_interact设为False用来提醒Plugin_Core删除数据。如果此插件根本没有互动功能，请不要加入此参数。