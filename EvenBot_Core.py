import asyncio
import websockets
import json
from EvenBot_API import EvenBotAPI
from EvenBot_Plugin_Core import PluginManager
def getPluginInfo():#导入触发词。请确保已初始化载入所有插件！！
    rc=manager.enumPlugins()
    for names in rc:
        text=manager.getText(names[0])
        actions[text]=names[0]
        textRules.append(text)
        # 另外：desc方法并没有使用，预留的，可自行发挥(原计划用作插件的描述，但是后面菜单改为自己手动画了XD)。
def update():
    #卸载所有插件
    global manager,textRules,actions
    manager2=PluginManager()
    rc=manager2.enumPlugins()#拷贝一份，不然manager删除的时候rc的长度会变的
    for names in rc:
        manager.unload_plugin(names[0])
    manager.clear()#清除EvenBot_Plugin_Core中的数据
    del manager,manager2,textRules,actions
    # 重新定义与初始化
    manager=PluginManager()
    manager.load_plugins()
    actions={}
    textRules=[]
    getPluginInfo()#重新获取插件触发词
async def websocket_client(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            jsonV=json.loads(message)
            if(jsonV['post_type']=='message'):#只处理群消息
                if(jsonV['message_type']=='group'):
                    InteractInfo=manager.enumInteractInfo()
                    # 消息处理顺序：upd(指定刷新词)->互动消息(任意消息内容)->普通消息(符合触发词)
                    #            为了防止冲突，三者中只能处理一种
                    if(jsonV['message']=='upd'):
                        update()
                        Api.SendGroupMsg(jsonV['group_id'],f"😋重载完成，现在有{len(manager.plugins)}个插件。🤖")
                    else:
                        # 此人目前正在互动消息模式
                        if str(jsonV['group_id']+jsonV['sender']['user_id']) in InteractInfo:
                            # 处理互动信息，之后不再按普通信息处理
                            data={'message':jsonV['message'],
                                            'group_id':jsonV['group_id'],
                                            'PluginObjs':manager,
                                            'textRules':textRules,
                                            'from_id':jsonV['sender']['user_id'],
                                            'nick':jsonV['sender']['nickname'],
                                        }
                            # 向perfom_action_interact中传入对应消息数据
                            try:
                                        manager.perform_plugins_actions(InteractInfo[str(jsonV['group_id']+jsonV['sender']['user_id'])]['task'],data)
                            # 最多同时执行5条，可在EvenBot_Plugin_Core.py中修改。
                            except MemoryError as e:
                                        Api.SendGroupMsg(jsonV['group_id'],"您最多同时执行5个插件😋\n请爱护您的奴。")
                        
                        else:
                            # 此处为普通消息，遍历触发词数组，检查前缀是否符合
                            global actions
                            for txts in textRules:
                                if(jsonV['message'][0:len(txts)]==txts):
                                    jsonV['message']=jsonV['message'].replace(txts,"",1)
                                    #把触发词删除，留下后面的消息内容，方便插件处理。
                                    data={'message':jsonV['message'],
                                            'group_id':jsonV['group_id'],
                                            'PluginObjs':manager,
                                            'PluginData':manager.enumPlugins(),
                                            'textRules':textRules,
                                            'from_id':jsonV['sender']['user_id'],
                                            'nick':jsonV['sender']['nickname'],
                                        }
                                    # 将任务投递到PluginManager，由PluginManager进行管理
                                    try:
                                        manager.perform_plugins_actions(actions[txts],data)
                                    except MemoryError as e:
                                        Api.SendGroupMsg(jsonV['group_id'],"您最多同时执行5个插件😋\n请爱护您的奴。")
                                
if __name__ =="__main__":
    # 定义和初始化变量
    manager=PluginManager()
    manager.load_plugins()
    actions={}
    textRules=[]
    Api=EvenBotAPI()
    getPluginInfo()
uri = "ws://127.0.0.1:1146"
asyncio.get_event_loop().run_until_complete(websocket_client(uri))# 连接WS