import json

from flask import Flask
from flask_restplus import Api, Resource
from flask_restplus import reqparse
import uuid

from template.order_drink_temp import OrderCoffeeIdentify
from scene_manage.scene_manage_dialogue import SceneManage


app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('sentence', type=str, help='输入的句子', required=True)

parser.add_argument('token', type=str, help='验证token，用于权限验证，暂时无', location='headers')
parser.add_argument('machine_state', type=str, help='机器人状态', location='form')
parser.add_argument('machine_state', type=str, help='机器人状态', location='form')
parser.add_argument('machine_id', type=str, help='机器人id', location='form')
parser.add_argument('condition_id', type=str, help='限制条件id', location='form', default='')
parser.add_argument('session_id', type=str, help='会话（上下文）id', location='form', default='')
parser.add_argument('city', type=str, help='城市', location='form', default='上海')
parser.add_argument('multi_input', type=str, help='多模态输入, 请输入json字段', location='form')


@api.route('/ask')
class Answer(Resource):
    def post(self):
        # 接受传过来的数据
        post_data = parser.parse_args()
        sentence = post_data.get('sentence')
        # 语音错别字纠正
        sentence = self.char_mapping(sentence)
        yes = ['是的', '是', '对', '对的', '小风同学', '你好']
        if sentence in yes:
            # 表示已经和客户确认好订餐内容
            return self.order_ok(sentence, yes)
        else:
            # 将得到的数据经过模板处理
            tem_result = OrderCoffeeIdentify().identify(sentence)
            # print(tem_result)
            # 将处理后的结果进行多轮多订单处理
            answer = SceneManage().scene_manage(sentence, tem_result)
            if not answer:
                return {"answer": "对不起，我没有听懂你说的话，请你换一种说话"}
            return answer

    def order_ok(self, sentence, yes):
        # 表示已经和客户确认好订餐内容
        if sentence == '你好':
            with open('finish_order.txt', 'a+', encoding='utf-8') as fc:
                fc.truncate(0)
            # 删除一开始订单
            with open('order.txt', 'a+', encoding='utf-8') as fc:
                fc.truncate(0)
            # 删除 session_id
            with open('session.txt', 'a+', encoding='utf-8') as fc:
                fc.truncate(0)
            return {"answer": "你好呀，我是智能语音咖啡师，你想喝什么你都可以跟我说"}
        elif sentence in yes:
            res = []
            with open('finish_order.txt', 'r', encoding='utf-8') as fr:
                data = []
                for line in fr.readlines():
                    line = line.strip()
                    res.append(line)
                    if line:
                        d = {"number": line[0:2], "size": line[2:5], "coldorhot": line[5:7], "product": line[7:]}
                        data.append(d)

            response = ','.join(res)
            # 删除已经完成的订单
            with open('finish_order.txt', 'a+', encoding='utf-8') as fc:
                fc.truncate(0)
            # 删除一开始订单
            with open('order.txt', 'a+', encoding='utf-8') as fc:
                fc.truncate(0)
            # 删除 session_id
            with open('session.txt', 'a+', encoding='utf-8') as fc:
                fc.truncate(0)
            if response:
                datas = {"data": data, "answer": "好的，这就去给你准备" + response + ",请稍等..."}
                return datas
            else:
                return {"answer": "你好呀，我是智能语音咖啡师，你想喝什么你都可以跟我说"}

    def char_mapping(self, sentence):
        with open('mapping.txt', 'r', encoding='utf-8') as fr:
            sfs, sts = [], []
            for line in fr.readlines():
                sf, st = line.strip().split(',')
                sfs.append(sf)
                sts.append(st)

        for i, x in enumerate(sfs):
            if x in sentence:
                sentence = sentence.replace(x, sts[i])
        return sentence


if __name__ == '__main__':
    HOST = '10.8.108.59'
    PORT = 8090
    # 删除已经完成的订单
    with open('finish_order.txt', 'a+', encoding='utf-8') as fc:
        fc.truncate(0)
    # 删除一开始订单
    with open('order.txt', 'a+', encoding='utf-8') as fc:
        fc.truncate(0)
    # 删除 session_id
    with open('session.txt', 'a+', encoding='utf-8') as fc:
        fc.truncate(0)
    app.run(debug=True, host=HOST, port=PORT)

