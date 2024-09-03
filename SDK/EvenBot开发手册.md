# EvenBot开发手册

写好的插件请放在Plugin\分类\插件.py，刷新后自动载入。

> **提示**
> 
> 插件系统现在写的并不完美！欢迎自行优化，欢迎交流！

## data与return解析

> Source: SDK\python_sdk.py

```python
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
        return None
```

`YourPlugin` 名必须独一无二，否则载入时会发生错误

`getText` 为触发词，如果你希望任意消息触发，可以return ""

`perform_action` 为插件执行入口

`data` 中的数据为

        `message` STRING. 消息正文

        `group_id` INT. 来源群号

>         `PluginObjs` PluginManager. EvenBot的插件管理器实例，可执行对应方法
> 
>         `textRules` STRING[]. 返回所有触发词
> 
>         以上两个数据是为了做菜单而设计的。

        `from_id` INT. 发送人QQ号

        `nick` STRING. 发送人昵称

`return` NONE/DICT. 返回值必须为None或字典，不可为其他类型。

字典中以下键值有效：

`return`

        `need_interact` BOOL. 设置的互动模式状态

                此键值有三种形态：True (启动/继续互动)，False (删除互动操作)，没有此键值 (按照普通消息处理)

                有关互动模式，请看这里。

        `from_id` INT. 回执发送人QQ号

        `group_id` INT. 回执发送群号

        `need_update` BOOL. 是否需要刷新机器人(重载所有插件)





## 互动插件

与普通插件不同的一点是，互动插件还需要`perform_action_interact`方法用来执行启动互动消息后的操作。

> Source: Plugin\Interact\interact.py

```python
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
```

互动信息需要您自行存储，本Demo中已提供相关方法，请自行查看。

每个互动功能的用户使用唯一UID(各个群)。

考虑到事件极小性(bushi)，UID为群号与QQ号的和。

### 逻辑

用户发送含有调用互动插件的触发词(即 `perform_action`) -> 输入互动消息(互动消息不需要触发词)->执行每一步操作，若中途退出需要回复exit->任务完成

### 注意

`perform_action` 中不宜在**提示用户是互动消息**后放置过多代码，否则容易造成步骤冲突。

如果用户在互动模式时，必须退出或完成才可以使用普通功能。

每一步在执行时，该群该用户不允许使用机器人。














