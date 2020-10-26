import socket

import requests
import uuid


class BaiduPartner(object):

    def get_intention(self, sentence, client_id, client_secret, session, bot_session=''):
        access_token = self.get_access_tocken(client_id, client_secret)
        url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + access_token
        # 获取本机计算机名称
        hostname = socket.gethostname()
        # 获取本机ip
        ip = socket.gethostbyname(hostname)
        post_data = {
            # 'bot_session': bot_session,
            'log_id': uuid.uuid1().hex,
            'request': {'bernard_level': 1,
                        'client_session': '{"client_results":"", "candidate_options":[]}',
                        'query': sentence,
                        'query_info': {'asr_candidates': [], 'source': 'KEYBOARD', 'type': 'TEXT'},
                        'updates': '',
                        'user_id': ip
                        },
            # 'bot_id': '1050870',
            'session_id': session,
            'service_id': 'S36493',
            'version': '2.0',
        }
        response = requests.post(url, json=post_data)
        if response:
            res = response.json()
            print('百度返回结果是： %s' %res)
            # print(res['result']['response_list'][0]['action_list'][0]['say'])
            # 将回答中的意图是回答的话放入到一个数组中
            try:
                intent_and_say = res['result']['response_list'][0]['action_list'][0]['say'].split('/')
                intent = ''
                if len(intent_and_say) > 1:
                    intent = intent_and_say[0]
                    say = intent_and_say[1]
                else:
                    say = intent_and_say[0]
                # 拿到当前对话的session
                session_id = res['result']['session_id']
                if res['error_code'] == 0 and intent != '':
                    # 将词槽的值提取出来放入到 records中 [{'user_number': '一杯'}, {'user_type': '美式'}]
                    records_temp = res['result']['response_list'][0]['schema']['slots']
                    records = [{record['name']: record['original_word']} for record in records_temp]
                    return {"intent": intent, "records": records, "answer": say, "session_id": session_id}
                return {}
            except:
                return {}
        else:
            return {}

    def get_access_tocken(self,client_id, client_secret):
        """"""
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
            client_id, client_secret)
        response = requests.get(host)
        if response:
            res = response.json()
            return res['access_token']


if __name__ == '__main__':
    API_Key = "cV3kqG8YldcxF7fRG0TlsIXf"
    Secret_Key = "uY9vdZadvGKi6XpEC4QIGxEPv41ljpH9"
    result = BaiduPartner().get_intention('一杯大杯美式', API_Key, Secret_Key, '7dfdfc',
                                          'service-session-id-1602679349495-b8a8f3c2-0e1a-11eb-b3e4-e78c31807367')
    print(result)