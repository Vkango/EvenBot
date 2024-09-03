from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
import time
Api=EvenBotAPI()
InteractData={}
class Interact_TEST(PluginInterface):
    def getDesc(self):
        return "互动型插件示例"
    def getText(self):#此处触发词为引起功能的触发词，用户第二次回复的内容可能不包含触发词，但仍要触发。
        return "interact1"
    def perform_action(self,data):
        # 请仔细查看data中包含了什么数据，另外，message已去掉触发词。
        Api.SendGroupMsg(data['group_id'],"现在将开始互动！")
        USER_DATA={}
        USER_DATA['Step']=0
        InteractData[data['group_id']+data['from_id']]=USER_DATA
        # 这一步不应该执行过多的操作，容易造成步骤冲突。
        # 内部已经做了限制，必须按步骤来（此场景下单个步骤可能需要执行较长时间）
        # 因此第一步务必简短，尽快告诉Plugin_Core要进行互动！
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
            Api.SendGroupMsg(data['group_id'],"您现在正在第一步！这一步需要花费5s！")
            time.sleep(5)
            Api.SendGroupMsg(data['group_id'],"第一步执行成功！接下来将执行第二步，退出请回复exit")
        if USER_DATA['Step']==1:
            Api.SendGroupMsg(data['group_id'],"您现在正在第二步！退出请回复exit")
        if USER_DATA['Step']==2:
            Api.SendGroupMsg(data['group_id'],"任务完成！")
        

        # 别忘了加一步！~
        USER_DATA['Step']+=1
        # 覆写全局变量
        InteractData[data['group_id']+data['from_id']]=USER_DATA
        return {'need_interact': False,"group_id":data['group_id'],"from_id":data['from_id']} if USER_DATA['Step'] == 3 else {"need_interaction":True,"group_id":data['group_id'],"from_id":data['from_id']}
        # 注意：此处need_interact设为False用来提醒Plugin_Core删除数据。如果此插件根本没有互动功能，请不要加入此参数。