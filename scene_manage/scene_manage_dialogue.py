import uuid
import time
from collections import ChainMap

from nlp_interface.baidu import BaiduPartner


class SceneManage(object):
    def scene_manage(self, sentence, tem_result):
        self.API_Key = "cV3kqG8YldcxF7fRG0TlsIXf"
        self.Secret_Key = "uY9vdZadvGKi6XpEC4QIGxEPv41ljpH9"
        flag = 0
        # 如果抽取出来为空，则原始句子直接请求unit接口
        if not tem_result:
            # 请求百度的unit接口
            session = uuid.uuid1().hex
            result = BaiduPartner().get_intention(sentence, self.API_Key, self.Secret_Key, session, 'bot_session')
            if result.get('records'):
                stress = {'answer': '你说的我听不懂，请您换一种说法'}
                return stress
            return {"answer": result.get('answer')}
        # 确认意图是删除
        if tem_result[0].__contains__("del"):
            flag = 1
            with open('order.txt', 'r', encoding='utf-8') as fr:
                res_order = self.read_file('order.txt')
                # 判断删除的是已完成的还是未完成的
                if tem_result and res_order and tem_result[0].get('product') in res_order[0] or not tem_result[0].get('product'):
                    res_sess = self.read_file('session.txt')
                    if len(res_sess) > 1:
                        self.write_file('session.txt', res_sess[1:])
                    # 删除当前订单之后，未完成订单还有，则继续提问
                    if len(res_order) > 1:
                        self.write_file('order.txt', res_order[1:])
                        last_session = uuid.uuid1().hex
                        return self.req_baidu(flag, res_order[1], last_session)
                    # 删除之后没有订单，则直接返回结果
                    else:
                        with open('order.txt', 'a+', encoding='utf-8') as fc:
                            fc.truncate(0)
                        orders = self.read_file('finish_order.txt')
                        if len(orders) != 0:
                            stress = ''
                            for order in orders:
                                stress += order + ','
                            if len(stress) != 0:
                                stress = '好的，请确认下你要的是：' + stress[:-1] + '吗?'
                                return {'answer': stress}
                        else:
                            return {'answer': '订单已经删除，请问你还想点什么吗？我们有美式，拿铁，奶茶，咖啡'}
                # 从已完成订单中删除
                else:
                    res = []
                    lines = self.read_file('finish_order.txt')
                    for line in lines:
                        if tem_result[0].get('product', '') not in line:
                            res.append(line)
                    self.write_file('finish_order.txt', res)
                    if len(lines) == len(res):
                        return {"answer": "对不起，你并没有订" + tem_result[0].get('product', '')}
                    if len(self.read_file('order.txt')) == 0:
                        stress = ','.join(res)
                        if len(stress) != 0:
                            return {"answer": "好的，请确认下你要的是：" + stress + "吗?"}
                        else:
                            return {'answer': '订单已经删除，请问你还想点什么吗？我们有美式，拿铁，奶茶，咖啡'}

        # 确认意图是修改
        if tem_result[0].__contains__("upd"):
            flag = 1
            if tem_result[0].get('size'):
                # 将未完成订单第一行换了
                with open('order.txt','r',encoding='utf-8') as fr:
                    res = []
                    for i, line in enumerate(fr.readlines()):
                        print(12111)
                        print(line.strip())
                        print(tem_result[0].get('size'))
                        if i == 0:
                            line = line.replace(line[2:5], tem_result[0].get('size'))
                        res.append(line.strip())
                print(res)
                self.write_file('order.txt', res)
                with open('order.txt', 'r', encoding='utf-8') as fr:
                    order_one = fr.readline().strip()
                    last_session = uuid.uuid1().hex
                return self.req_baidu(flag, order_one, last_session)

        # 将句子拼接在一起
        orders, slot = SceneManage().combined_order(tem_result)
        # 判断此次问话是不是词槽收集
        if slot:
            order_one = slot[0]
            with open('session.txt', 'r', encoding='utf-8') as fr:
                last_session = fr.readline().strip()
            return self.req_baidu(flag, order_one, last_session)
        elif orders:
            flag = 1
            with open('order.txt', 'r', encoding='utf-8') as fr:
                order_one = fr.readline().strip()
                last_session = uuid.uuid1().hex
            return self.req_baidu(flag, order_one, last_session)
        else:
            res_fin_order = self.read_file('finish_order.txt')
            stress = ','.join(res_fin_order)
            answer = '好的，请确认下你要的是：' + stress + '吗?'
            return {'answer': answer}
    # 组合订单
    def combined_order(self, tem_result):
        # 输入的是订单
        # print(123)
        print(tem_result)
        if tem_result[0].get('product', '') != '':
            res = []
            for sentence in tem_result:
                i = 0
                str = ''
                if sentence.get('number'):
                    i += 1
                    str += sentence.get('number')
                if sentence.get('coldorhot'):
                    i += 1
                    str += sentence.get('coldorhot')
                if sentence.get('size'):
                    i += 1
                    str += sentence.get('size')
                if sentence.get('product'):
                    i += 1
                    str += sentence.get('product')
                # 当一句话条件足够时
                if i < 4:
                    res.append(str)
                else:
                    res_order = self.read_file('finish_order.txt')
                    res_order.append(str)
                    self.write_file('finish_order.txt', res_order)
            str = '\n'.join(res)
            # 首先判断里面是否有订单，有的话写入到第一行，没有的话，直接将该订单存放进来
            with open('order.txt', 'r+', encoding='utf-8') as f:
                lines = f.read()
                f.seek(0, 0)
                f.write(str + '\n' + lines)
            return res, ''
        # 输入的是条件槽值
        else:
            res = []
            for sentence in tem_result:
                number = sentence.get('number', '')
                size = sentence.get('size', '')
                cold_or_hot = sentence.get('coldorhot', '')
                s = number + size + cold_or_hot
                res.append(s)
            return '', res

    # 订单管理
    def manage_order(self, records):
        session_id = uuid.uuid1().hex
        # 将已经完成的订单拼接成字符串
        slots = records[0]
        for i in range(0, len(records)):
            slot = records[i]
            z = ChainMap(slots, slot)
            slots = z
        if slots.get('user_size') == '大杯':
            slots.__setitem__('user_size', '大杯的')
        if slots.get('user_size') == '小杯':
            slots.__setitem__('user_size', '小杯的')
        resss = slots.get('user_number') + slots.get('user_size') + slots.get('user_coldorhot') + slots.get('user_type')
        # 将完成的订单和之前完成的订单写进文件
        orders = self.read_file('finish_order.txt')
        orders.append(resss)
        self.write_file('finish_order.txt', orders)

        # 将完成的订单从未完成的订单文件中移除
        # 1. 将第一个订单之外的订单读取出来
        with open('order.txt', 'r', encoding='utf-8') as fr:
            res = []
            for i, v in enumerate(fr.readlines()):
                if i != 0:
                    res.append(v.strip())
        # 如果没有订单了，则结束
        stress = ''
        if len(res) == 0:
            for order in orders:
                stress += order + ','
            return '', stress[:-1]

        # 2. 第一条移除，其他写入
        with open('order.txt', 'w', encoding='utf-8') as fw:
            for order in res:
                fw.write(order)
        return session_id, stress

    def finish_order(self, stress):
        stress = '好的，请确认下你要的是：' + stress + '吗?'
        # 删除原始订单
        with open('order.txt', 'a+', encoding='utf-8') as fc:
            fc.truncate(0)
        # 清空session_id
        with open('session.txt', 'a+', encoding='utf-8') as fc:
            fc.truncate(0)
        return stress

    def unfinish_order(self, session_id):
        # 完成了订单，删除第一行session
        with open('session.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            res = []
            for i, line in enumerate(lines):
                if i != 0:
                    res.append(line.strip())

        with open('session.txt', 'w', encoding='utf-8') as fw:
            # 若还有，则去除第一行
            if len(res) != 0:
                stress = '\n'.join(res)
                fw.write(stress)
            # 如果里面只有一个订单，则直接清除
            else:
                with open('session.txt', 'a+', encoding='utf-8') as fc:
                    fc.truncate(0)
        # 读取第二个订单
        with open('order.txt', 'r', encoding='utf-8') as fr:
            res = []
            for i, v in enumerate(fr.readlines()):
                if i == 0:
                    res.append(v.strip())
        order_one = ''.join(res)
        time.sleep(1)
        result = BaiduPartner().get_intention(order_one, self.API_Key, self.Secret_Key, session_id, 'last_session')
        session_id = result.get('session_id')
        return result, session_id

    def req_baidu(self, flag, order_one, last_session):
        # 请求竹简的接口
        result = BaiduPartner().get_intention(order_one, self.API_Key, self.Secret_Key, last_session, 'last_session')
        if flag == 1:
            session_id = result.get('session_id')
        else:
            session_id = ''
        # 若所需要的槽值填满了，则更换session_id
        print('result.get(records)的值是： %s' % result.get('records'))
        if result.get('records') and len(result.get('records')) == 4:
            session_id, stress = self.manage_order(result.get('records'))
            # 说明订单已经全部处理完
            if stress:
                stress = self.finish_order(stress)
                return {"answer": stress}
            # 说明后面还有订单,则重新生成session再继续问
            else:
                result, session_id = self.unfinish_order(session_id)
        # 如果session_id有值，说明又有一个新的对话session_id
        else:
            try:
                records = result.get('records')
                slots = records[0]
                for i in range(0, len(records)):
                    slot = records[i]
                    z = ChainMap(slots, slot)
                    slots = z
                if slots.get('user_size') == '大杯':
                    slots.__setitem__('user_size', '大杯的')
                if slots.get('user_size') == '小杯':
                    slots.__setitem__('user_size', '小杯的')
                resss = slots.get('user_number', '') + slots.get('user_size', '') + slots.get('user_coldorhot',
                                                                                              '') + slots.get(
                    'user_type', '')
                with open('order.txt', 'r', encoding='utf-8') as fr:
                    orders = []
                    for i, line in enumerate(fr.readlines()):
                        if i == 0:
                            line = resss
                        orders.append(line.strip())
                self.write_file('order.txt', orders)
            except:
                return {"answer": "对不起，我没有听懂你说的话，请你换一种说话"}
        if session_id:
            with open('session.txt', 'r+', encoding='utf-8') as fr:
                lines = fr.read()
                fr.seek(0, 0)
                # 如果session.txt有值，则一起写入
                if lines:
                    fr.write(session_id + '\n' + lines)
                else:
                    fr.write(session_id)

        return {"answer": result.get('answer')}


    # 将文件读取出来放入到列表中
    def read_file(self, path):
        res = []
        with open(path, 'r', encoding='utf-8') as fr:
            for line in fr.readlines():
                res.append(line.strip())
        return res

    # 将数组写入到文件中 lines为列表
    def write_file(self, path, lines):
        lines = '\n'.join(lines)
        with open(path, 'w', encoding='utf-8') as fw:
            for line in lines:
                fw.write(line)
