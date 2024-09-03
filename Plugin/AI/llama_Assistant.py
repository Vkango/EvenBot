# code from YouZikua
# <!> 此源码非原创，感谢YouZikua大蛇分享😍
gpt_response=""
import json
import requests
import os
from plugin_interface import PluginInterface
from EvenBot_API import EvenBotAPI
os.environ["HTTP_PROXY"] = "http://127.0.0.1:9890"
os.environ["HTTP_PROXYS"] = "http://127.0.0.1:9890"

host = ('localhost', 8888)

prompt = """You are a helpful assistant""" # 你的prompt
gpt_message=[{"role": "system", "content":prompt},]
gpt_context=""
url = "https://deepinfra.com"
default_model = 'meta-llama/Meta-Llama-3.1-405B-Instruct' # 模型 在https://api.deepinfra.com/models上有

def get_models(models):
    if not models:
        url = 'https://api.deepinfra.com/models/featured'
        models = requests.get(url).json()
    return models

def chat(
    model: str,
    messages: str,
    proxy: str = None,
    timeout: int = 120,
    auth: str = None,
    **kwargs
) -> str:
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://deepinfra.com',
        'Referer': 'https://deepinfra.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Deepinfra-Source': 'web-embed',
        'accept': 'text/event-stream',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    if auth:
        headers['Authorization'] = f"bearer {auth}" 
            
    json_data = {
        'model'      : model,
        'messages'   : messages,
        'stream'     : False,
        'temperature': 0.8,
        'max_tokens' : 100000,
    }
    response=requests.post('https://api.deepinfra.com/v1/openai/chat/completions',json=json_data,headers=headers)
    text=""
    try:
        text = json.loads(response.text).get("choices", [{}])[0].get("message", {}).get("content")
    except Exception as e:
        print(e)
    return text

def chatt(x, i, t):
    global gpt_context, prompt, gpt_message
    if t:
        gpt_message.append({"role": "user", "name": "系统", "content": x})
    else:
        gpt_message.append({"role": "user", "name": "玩家", "content": x})
    result = chat(default_model, gpt_message)
    gpt_message.append({"role": "assistant", "name": "AI", "content": result})
    return result


Api=EvenBotAPI()
class llama(PluginInterface):
    def getDesc(self):
        return "关于"
    def getText(self):
        return "[CQ:at,qq=2647345219] "
    def perform_action(self,data):
        msg_id=json.loads(Api.SendGroupMsg(data['group_id'],"请稍候..."))['data']['message_id']
        Api.SendGroupMsg(data['group_id'],chatt(data['message'], 0, False)) 
        Api.RecallMsg(msg_id)
        