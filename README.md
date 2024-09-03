# 👋 欢迎

本机器人为练习Python制作，代码并不规范，欢迎优化，欢迎交流，共同进步！

# ⚡ 快速开始

请使用支持OneBot协议机器人框架，并开启正向WebSocket协议以及HTTP协议。

默认端口地址 (请直接修改源码，还未加入设置项QAQ)：

HTTP：1145

正向WebSocket：1146

运行EvenBot_Core.py即可启动机器人。

# 📂 加载插件

请将插件文件放置在Plugin文件夹下的分类文件夹中(但不要放在根目录下)，重新启动或刷新后可自动加载已知插件。

# 🎈 开发

请参阅SDK文件夹下的开发文档。

# 🚀 加油

学业问题，机器人维护可能并不及时。

一些体验优化待办如下：

1. 引入设置项 (EvenBot_Config)

2. 引入权限系统 (EvenBot_Auth)

3. 插件不能溯源 (不能找在哪里加载的)

4. 插件注册：建议直接用文本的方法查找是否有PluginInterface，加载需要额外的时间。(但此方法不严谨)

5. 下载脚本：使用互动消息把downloadScript和SetAllow联动

6. EmojiKitchen：判断是否为两个Emoji的方法

7. 另外插件命名不一致，“脚本”“插件”可能没分开

本人初学Python，水平较低QAQ

# 📄 引用及参考

hanyu.baidu.com (百度汉语客户端API，引用于Baidu_Hanyu.py)

Deepinfra (deepinfra_api，引用于llama_Assistant.py，非原创，感谢YouZikua提供的代码)

c.tieba.baidu.com (百度贴吧客户端API，引用于ps_bar_post.py，Sign算法非原创(没有找到原作者，欢迎原作者联系我进行修改))

emojikitchen.dev (Google Emoji Kitchen复刻，项目地址https://github.com/xsalazar/emoji-kitchen，引用于EmojiKitchen.py)

garbage.json (垃圾分类数据，项目地址https://github.com/alexayan/garbage-classification-data，引用于garbage.json、garbage.py)

MasterGo (莫高设计，mastergo.com，用于设计菜单)

感谢以上项目支持！✨

# 💭 后记

GitHub: Vkango (Lonyou)

声明：此项目仅供学习交流使用，出现的任何后果作者概不负责！可在保留作者信息的前提下自由转载，遵循MIT开源协议。

觉得有用可自取，觉得没用可无视。

再次感谢！
