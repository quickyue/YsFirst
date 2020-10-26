# -*- coding:utf-8 -*-
import os, time
from multiprocessing import Process

class MyProcess(Process):
    def __init__(self):
        Process.__init__(self)

    def run(self):
        print("子进程开始>>> pid={0},ppid={1}")
        time.sleep(2)
        print("子进程终止>>> pid={}")


def main():
    print("主进程开始>>> pid={}")
    myp = MyProcess()
    myp.start()
    print("主进程终止")


if __name__ == '__main__':
    main()

# line = '一杯大杯的美式'
# print(line.replace(line[2:5], '小杯的'))
# s = '没事不要了'
# with open('mapping.txt','r',encoding='utf-8') as fr:
#     Sfs, Sts = [], []
#     for line in fr.readlines():
#         Sf, St = line.strip().split(',')
#         Sfs.append(Sf)
#         Sts.append(St)
#
# for i, x in enumerate(Sfs):
#     if x in s:
#         s = s.replace(x, Sts[i])
#
# print(s)

# 获取本机计算机名称
# hostname = socket.gethostname()
# # 获取本机ip
# ip = socket.gethostbyname(hostname)
# print(ip)
# with open('order.txt', 'r', encoding='utf-8') as fr:
#     data = []
#     for line in fr.readlines():
#         line = line.strip()
#         d = {"number":line[0:2], "size": line[2:5], "coldorhot": line[5:7], "product": line[7:]}
#         data.append(d)

# #列表L1包含3个元素，每个元素都是字典形式，下列代码将这3个元素“合并”成一个字典
# from collections import ChainMap
#
# L1 = [{"a": "AAA"}, {"b": "BBB"}, {"c": "CCC"}]
# # print(ChainMap(L1))
#
# #获取元素个数
# x = L1[0]
# #利用循环将字典依次"合并"
# for i in range(1, len(L1)):
#     y = L1[i]
#     z = ChainMap(x, y)
#     x = z
# print(x)
# print(x.get("a")+x.get("b")+x.get("c"))
# print(x.get("b"))
# print(x.get("c"))
#
#
# #temp = [{'product': '美式', 'number': '一杯', 'size': '大杯的'}]
# records = [{'user_coldorhot': '热的'}, {'user_size': '大杯的'}, {'user_number': '一杯'}, {'user_type': '拿铁'}]
#
# res = []
# for r in records:
#     res.extend(r)
# # print(res)
# resss = []

# for sentence in records:
#     str = ''
#     if sentence.get('user_number', ''):
#         str += sentence.get('user_number', '')
#     if sentence.get('user_size', ''):
#         str += sentence.get('user_size', '')
#     if sentence.get('user_coldorhot', ''):
#         str += sentence.get('user_coldorhot', '')
#     if sentence.get('user_type', ''):
#         str += sentence.get('user_type', '')
#     resss.append(str)
# resss = ''.join(resss)
# print(resss)



# s = {"1": "879", "s": "88"}
# if s.__contains__("s"):
#     print(12)
# print(s.__contains__("s"))
# a = {'product': '美式', 'number': '一杯', 'size': '大杯的'}
# print(a.__contains__('number'))


# a = {'sdf', 'asdf', 'adsf', 'dfs', 'dfs', 'dfs', 'dfs'}
# for i in a:
#     if '' in i:
#         print(i)

# session_id = uuid.uuid1().hex
# with open('session.txt', 'r+', encoding='utf-8') as fr:
#     lines = fr.read()
#     fr.seek(0, 0)
#     fr.write(session_id + '\n' + lines)
# with open('order.txt','r+',encoding='utf-8') as f :
#     lines = f.read()
#     f.seek(0, 0)
#     f.write('ttt'+'\n'+lines)


# with open('order.txt', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     res = []
#     for i, line in enumerate(lines):
#         if i != 0:
#             res.append(line.strip())
#     stress = '\n'.join(res)
#
# with open('order.txt', 'w',encoding='utf-8') as fw:
#     fw.write(stress)


# with open('order.txt','r+',encoding='utf-8') as f :
#     lines = f.read()
#     f.seek(0, 0)
#     f.write('ttt'+'\n'+lines)


# temp = [{'product': '美式', 'number': '一杯', 'size': '大杯的'}]
# res = []
# for text in temp:
#     str = ''
#     if text.get('number'):
#         str += text.get('number')
#     if text.get('coldorhot'):
#         str += text.get('coldorhot')
#     if text.get('size'):
#         str += text.get('size')
#     if text.get('product'):
#         str += text.get('product')
#     res.append(str)
# strsss = '\n'.join(res)
# print(res)
# print(strsss)



# with open('order.txt','a+',encoding='utf-8') as fc:
#     fc.truncate(0)



# a = [{'user_coldorhot': '热的'}, {'user_number': '一杯'}, {'user_size': '大杯'}, {'user_type': '美式'}]
# b = [{'product': '', 'coldorhot': '热的'}]
# res = []
# for sentence in a:
#     number = sentence.get('user_number', '')
#     size = sentence.get('user_size', '')
#     cold_or_hot = sentence.get('user_coldorhot', '')
#     product = sentence.get('user_type', '')
#     s = number + size + cold_or_hot + product
#     res.append(s)
# print(res)
# print(''.join(res))
# lines = ['aa','ss','dd','ff']
# lines = ''.join(lines)
# with open('c.txt', 'w', encoding='utf-8') as fw:
#     for line in lines:
#         fw.write(line)

# with open('./order.txt', 'r', encoding='utf-8') as fr :
#     for i,v in enumerate(fr.readlines()):
#         print(i,v)
    # print(fr.readline().strip())

# a = {'product': '', 'coldorhot': '热的','product1': '','product2': '','product3': '','product4': '','product5': '','product6': '','product7': ''}
# for i,v in enumerate(a.values()):
#
#     print(i,v)

# a = 'service-session-id-1602678742253-4eb72ad4-0e19-11eb-8b5a-67da583455f5'
# b = 'service-session-id-1602678742253-4eb72ad4-0e19-11eb-8b5a-67da583455f5'
# print(a == b)

# class A(object):
#
#     def aaa(self):
#         rrr = [0]
#         res = self.ccc(rrr[-1])
#         rrr.append(res)
#         return res
#
#     def ccc(self, a):
#         x = uuid.uuid1().hex
#         return x
#
#
# if __name__ == '__main__':
#     res = A().aaa()