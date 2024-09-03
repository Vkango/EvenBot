import http
import json
class EvenBotAPI:
    def Api_SendReq(self,api,data):
        """ 发送请求POST """
        host="127.0.0.1"
        port=1145
        connect=http.client.HTTPConnection(host,port)
        url="/"+api
        data_json=json.dumps(data)
        headers={
        'Content-Type': 'application/json',
        'User-Agent': 'EvenBot'}
        connect.request("POST",url,body=data_json,headers=headers)
        res=connect.getresponse().read().decode()
        connect.close()
        return res

    def SendGroupMsg(self,groupid,msg):
        """ 发送群消息 """
        data1={"group_id":groupid,"message":msg}
        return self.Api_SendReq("send_group_msg",data1)
    def RecallMsg(self,msg_id):
        """ 撤回消息 """
        data1={"message_id":msg_id}
        return self.Api_SendReq("delete_msg",data1)
    