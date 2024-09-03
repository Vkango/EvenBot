# 请注意Emoji合成数据位于Temp\data.json，合成数据只存储了合成后表情的图片URL地址，而不是图片bin
# 源码原创，但此项目是Google GBoard中的功能分支
# data.json来自GitHub仓库https://github.com/xsalazar/emoji-kitchen
from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
Api=EvenBotAPI()
class EmojiKitchen(PluginInterface):
    def getDesc(self):
        return "EmojiKitchen.dev"
    def getText(self):
        return "emoji "
    def perform_action(self,data):
        text = data['message']
        if not len(text)==2 and not len(text)==3:
            # TODO:emoji单个表情字符可能不是1，也可能是2，也就是说两个表情len可能是2或3，目前没有方法完美判断。
            Api.SendGroupMsg(data['group_id'],"🤔你需要提供两个Emoji才可以进行操作。")#此代码未处理特殊情况。
            # 但是无伤大雅。
            return
        unicode_hex_positions = '_'.join("u"+format(ord(char), 'x') for char in text)#取出unicode位置，作为查找依据
        # TODO: 请更换目录名！！！！
        w=open("D:\\EvenBot\\Temp\\data.json","rb")
        src=str(w.read())
        w.close()
        loc1=src.find(unicode_hex_positions)
        if loc1==-1:
            text=reversed(text)
            unicode_hex_positions = '_'.join("u"+format(ord(char), 'x') for char in text)
            w=open("D:\\EvenBot\\Temp\\data.json","rb")
            src=str(w.read())
            w.close()
            loc1=src.find(unicode_hex_positions)
        #TODO: 优化上面的代码，减少文件读写次数
        if loc1==-1:
            Api.SendGroupMsg(data['group_id'],"😭我不会。")
            return
        #这里直接使用文本处理，用json也很方便，但我直接偷懒了，反正我们只要一个图片url  XD
        loc2=src.find("emojikitchen",loc1-30)
        Api.SendGroupMsg(data['group_id'],"[CQ:image,file=https://www.gstatic.com/android/keyboard/"+src[loc2:loc1]+unicode_hex_positions+".png]")