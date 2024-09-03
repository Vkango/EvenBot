import importlib.util
import os
import sys
import importlib
from EvenBot_API import EvenBotAPI
import threading
from plugin_interface import PluginInterface
global Active_Tasks
global Interact_Info
Active_Tasks=[]
Interact_Info={}
Api=EvenBotAPI()
class MultiThread(threading.Thread):
    def __init__(self,target,target_interact,name,data):
        threading.Thread.__init__(self)
        self.target=target
        self.name=name
        self.data=data
        self.target_interact=target_interact
    def run(self):
        #动全局任务列表要加锁 防止冲突 但我没加（逃
        try:
            # 先看是否是互动模式
            if str(self.data['group_id']+self.data['from_id']) in Interact_Info:
                if Interact_Info[str(self.data['group_id']+self.data['from_id'])]['end']==False:#之前的任务还未完成！
                    Api.SendGroupMsg(self.data['group_id'],"😥抱歉，请等上一步任务执行完成！")
                    return
                else:
                    # 互动模式进入下一步操作！
                    global Active_Tasks
                    task_name=str(len(Active_Tasks)+1)+". "+self.name # 你说得对，但我们确实就是这么命名的。
                    Active_Tasks.append(task_name)
                    # 执行任务状态设为false
                    Interact_Info[str(self.data['group_id']+self.data['from_id'])]={'end':False,'task':self.name}# 此处end task都要写上，不然数据就不全了！
                    recv=self.target_interact(self.data)#注意此处是target_interact
                    Interact_Info[str(self.data['group_id']+self.data['from_id'])]={'end':True,'task':self.name}
                    # 任务执行完成，允许下一步操作
                    # 删除互动完成的数据
                    if 'need_interact' in recv:
                        if recv['need_interact']==False:
                            del Interact_Info[str(self.data['group_id']+self.data['from_id'])]
                    print("Plugin finished. recv data: ",recv)
                    #recv为插件返回的数据，可以做分析(TODO: 处理need_update消息)
                    Active_Tasks.remove(task_name)# 这句别忘了！
                    return
            # 此处书写非互动模式互动代码
            task_name=str(len(Active_Tasks)+1)+". "+self.name
            Active_Tasks.append(task_name)
            recv=self.target(self.data)
            if not recv==None:
                if 'need_interact' in recv:
                    if recv['need_interact']==True:
                        Interact_Info[str(self.data['group_id']+self.data['from_id'])]={'end':True,'task':self.name}
                    #False情况在上面了。
            print("Plugin finished. recv data: ",recv)
            Active_Tasks.remove(task_name)
        except Exception as e:
            Api.SendGroupMsg(self.data['group_id'],"执行插件时发生异常😰\n"+str(e))
            Active_Tasks.remove(task_name)#这句别忘了！
    def enumCount(self):
        return Active_Tasks #返回活跃的插件列表，与PluginManager的方法对应，外部插件可以通过调用PluginManager方法间接访问Active_Tasks(详见tasklist.py)
class PluginManager:
    def __init__(self, plugin_dir='Plugin'):# 定义Plugin
        self.plugin_dir = plugin_dir
        self.plugins = {}

    def load_plugins(self):
        """ 动态加载 Plugin 目录下所有子目录 """
        # 注意：Plugin根目录下的插件不会被加载！
        for plugin_subdir in os.listdir(self.plugin_dir):# 找子文件夹
            plugin_path = os.path.join(self.plugin_dir, plugin_subdir)
            if os.path.isdir(plugin_path):
                self.load_plugins_from_subfolder(plugin_path)# 加载插件

    def load_plugins_from_subfolder(self, subdir):
        sys.path.append(subdir)  # 将插件子目录添加到模块搜索路径
        for module_name in os.listdir(subdir):
            if module_name.endswith('.py') and not module_name.startswith('_'):# 文件名不能以下划线开头
                module_name_without_ext = module_name[:-3]# 取出文件名以便加载
                module_spec = importlib.util.spec_from_file_location(module_name_without_ext, os.path.join(subdir, module_name))
                if module_spec and module_spec.loader:
                    module = importlib.util.module_from_spec(module_spec)
                    module_spec.loader.exec_module(module)
                    self.register_plugin(module)
            #TODO:功能建议 1.插件不能溯源(不能找在哪里加载的) 2.建议直接用文本的方法查找是否有PluginInterface，加载需要额外的时间。(但此方法不严谨)
    def register_plugin(self, module):
        """ 注册插件，检查是否有实现 PluginInterface 的类 """
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, type) and issubclass(attribute, PluginInterface) and attribute is not PluginInterface:
                plugin_class = attribute
                plugin_instance = plugin_class()  # 实例化插件
                self.plugins[attribute_name] = plugin_instance  # 使用类名作为字典的键

    def unload_plugin(self,target_plugin):
        """ 卸载插件 """
        if target_plugin in self.plugins:
            plugin_class = self.plugins[target_plugin]
            module_name = plugin_class.__module__
            importlib.invalidate_caches()
            if module_name in sys.modules:
                del sys.modules[module_name]
            del self.plugins[target_plugin]
        else:
            print(f"Plugin {target_plugin} not found.") # 怎么可能卸载失败，一定是你名字的问题..(bushi
    def reload_plugin(self, target_plugin):
        """ 重载插件 """
        if target_plugin in self.plugins:
            #获取插件类
            plugin_class = self.plugins[target_plugin]
            module_name = plugin_class.__module__
            importlib.invalidate_caches()
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            try:
                module = importlib.import_module(module_name)
                importlib.reload(module)
                if hasattr(module, target_plugin):
                    # 重新实例化插件
                    plugin_instance = getattr(module, target_plugin)()
                    self.plugins[target_plugin] = plugin_instance  # 更新字典中的实例
                else:
                    print(f"Class {target_plugin} not found in the reloaded module.")
            except Exception as e:
                print(f"An error occurred while reloading the plugin: {e}")
        else:
            print(f"Plugin {target_plugin} not found.")
    def getDesc(self,target_plugin):
        if target_plugin in self.plugins:
            try:
                return self.plugins[target_plugin].getDesc()
            except Exception:
                return "" #None
        else:
            print(f"Plugin {target_plugin} not found or not loaded.")
    def getText(self,target_plugin):
        if target_plugin in self.plugins:
            try:
                return self.plugins[target_plugin].getText()
            except Exception:
                return ""
        else:
            print(f"Plugin {target_plugin} not found or not loaded.")
    def perform_plugins_actions(self, target_plugin, data):
        """ 执行指定插件的动作 """
        if target_plugin in self.plugins:
            # 不得超过5个并行操作
            if(len(Active_Tasks)<5):
                try:
                    thread1=MultiThread(target=self.plugins[target_plugin].perform_action,target_interact=self.plugins[target_plugin].perform_action_interact,data=data,name=target_plugin)
                except:
                    thread1=MultiThread(target=self.plugins[target_plugin].perform_action,target_interact=self.plugins[target_plugin].perform_action,data=data,name=target_plugin)
                thread1.start()
            else:
                raise MemoryError("最多同时执行5个任务。")
        else:
            print(f"Plugin {target_plugin} not found or not loaded.")
    def enumPlugins(self):
        """ 枚举插件 """
        return self.plugins.items()
    def enumActivePlugins(self):
        """ 枚举活跃插件列表 """
        return Active_Tasks
    def enumInteractInfo(self):
        """ 获取互动消息信息 """
        return Interact_Info
    def clear(self):
        """ 清除内部变量 """
        global Active_Tasks,Interact_Info
        del Active_Tasks,Interact_Info
        Active_Tasks=[]
        Interact_Info={}