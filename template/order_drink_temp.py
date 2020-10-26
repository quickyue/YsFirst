import re
from copy import deepcopy


class TemplatePares(object):

    def __init__(self, tempalte, keys=None, result=None):
        """"""
        if keys is None:
            keys = {}
        # 正则表达式
        self.temp = tempalte
        # 主键排序
        self.keys = self.order_keys(keys)
        # 生成一个正则表达式
        self.pattern = self.render_pattern()
        self.p = re.compile(self.pattern)
        # 结果
        self.res = result

    def order_keys(self, keys):
        """按照长度从大到小排序排序"""
        res = {}
        for k, v in keys.items():
            res[k] = sorted(v, key=lambda x: len(x), reverse=True)
        return res

    def cut_match(self, s):
        """"""
        g = self.p.match(s)
        if g:
            group_dict = g.groupdict()
            res = deepcopy(self.res)
            for dt in res:
                for k, v in dt.items():
                    dt[k] = group_dict.get(v, '')
            return s[g.end():], res
        else:
            return s, None

    def render_pattern(self):
        """生成正则表达式"""
        dt = {}
        m = re.findall('{[ a-zA-Z_0-9-]+}', self.temp)
        for k in m:
            k = re.sub('[{}]+', '', k)
            prefix_k = k.replace(' ', '').split('__')[0]
            dt[k] = "(?P<%s>%s)" % (k, '|'.join(self.keys[prefix_k]))
        return self.temp.format(**dt)


class OrderCoffeeIdentify(object):

    def __init__(self):
        """"""
        self.temp_list = [


            # 给我来两杯美式，一大一小
            TemplatePares(tempalte='(要|来|再来|我要|我想要|给我|给我来|帮我来)?{number__1}{product__1}{number__2}{size__1}(的)?{number__3}{'
                                   'size__2}(的)?',
                          keys={'product': ["美式", '拿铁', '奶茶', '咖啡'],
                                'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶',
                                           '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶'],
                                'size': ['大', '小', '大杯', '小杯', '大瓶', '小瓶']},
                          result=[
                              {'product': 'product__1', 'number': 'number__2', 'size': 'size__1'},
                              {'product': 'product__1', 'number': 'number__3', 'size': 'size__2'},
                          ]
                          ),




            # 给我来一杯美式，一杯奶茶，一杯咖啡,都要大杯的，都要热的
            TemplatePares(
                tempalte='(要|来|再来|我要|我想要|给我|给我来|帮我来)?{number__1}{product__1}{number__2}{product__2}{number__3}{product__3}(都要|全部都要)?{size__1}(都要|全部都要)?{coldorhot__1}',
                keys={'product': ["美式", '拿铁', '奶茶', '咖啡'],
                      'size': ['大', '小', '大杯', '小杯', '大瓶', '小瓶', '大杯的', '小杯的'],
                      'coldorhot': ['热的', '冷的','热','冷'],
                      'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶',
                                 '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶']},
                result=[
                    {'product': 'product__1', 'number': 'number__1', 'size': 'size__1', 'coldorhot': 'coldorhot__1'},
                    {'product': 'product__2', 'number': 'number__2', 'size': 'size__1', 'coldorhot': 'coldorhot__1'},
                    {'product': 'product__3', 'number': 'number__3', 'size': 'size__1', 'coldorhot': 'coldorhot__1'},
                ]
                ),



            # 我要一杯美式一杯拿铁，都是大杯的
            TemplatePares(tempalte='(来|我要|我想要|给我来|帮我来)?{number__1}{product__1}{number__2}{product__2}(都是|都要|都){size__1}(的)?',
                          keys={'product': ["美式", '拿铁', '奶茶', '咖啡'],
                                'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶',
                                           '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶'],
                                'size': ['大', '小', '大杯', '小杯', '大瓶', '小瓶']},
                          result=[
                              {'product': 'product__1', 'number': 'number__1', 'size': 'size__1'},
                              {'product': 'product__2', 'number': 'number__2', 'size': 'size__1'},
                                  ]
                          ),
            # 我要一杯美式一杯拿铁
            TemplatePares(
                tempalte='(来|我要|我想要|给我来|帮我来)?{number__1}{product__1}{number__2}{product__2}',
                keys={'product': ["美式", '拿铁', '奶茶', '咖啡'],
                      'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶',
                                 '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶']},
                result=[
                    {'product': 'product__1', 'number': 'number__1'},
                    {'product': 'product__2', 'number': 'number__2'},
                ]
                ),

            # 我要一杯美式
            TemplatePares(
                tempalte='(来|要|我要|我想要|给我来|帮我来)?{number__1}{product__1}',
                keys={'product': ["美式", '拿铁', '奶茶', '咖啡'],

                      'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶',
                                 '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶']
                      },
                result=[
                    {'product': 'product__1', 'number': 'number__1'},
                ]
                ),

            # 我要喝美式
            TemplatePares(
                tempalte='(来|要|我要|我想要|给我来|我想|帮我来)?(喝)?{product__1}',
                keys={'product': ["美式", '拿铁', '奶茶', '咖啡'],

                      'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶',
                                 '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶']
                      },
                result=[
                    {'product': 'product__1'},
                ]
            ),

            # 我要一杯大杯的美式
            TemplatePares(
                tempalte='(来|要|我要|我想要|给我来|帮我来)?{number__1}{size__1}{product__1}',
                keys={'product': ["美式", '拿铁', '奶茶', '咖啡'],
                      'size': ['大', '小', '大杯', '小杯', '大瓶', '小瓶'],
                      'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶',
                                 '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶']
                      },
                result=[
                    {'product': 'product__1', 'number': 'number__1', 'size': 'size__1'},
                ]
            ),

            # 我要一杯大杯的热的奶茶
            TemplatePares(
                tempalte='(来|要|我要|我想要|给我来|帮我来)?{number__1}{size__1}{coldorhot__1}{product__1}',
                keys={'product': ["美式", '拿铁', '奶茶', '咖啡'],
                      'size': ['大', '小', '大杯', '小杯', '大瓶', '小瓶', '大杯的', '小杯的'],
                      'coldorhot': ['热的', '冷的','热','冷'],
                      'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶',
                                 '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶']},
                result=[
                    {'product': 'product__1', 'number': 'number__1', 'size': 'size__1', 'coldorhot': 'coldorhot__1'},
                ]
            ),

            # 给我来一杯美式，一杯奶茶，一杯咖啡, 一杯拿铁，美式要大杯的热的，奶茶要小杯的冷的，咖啡要大杯的热的，拿铁要小杯的冷的
            # TemplatePares(
            #     tempalte='(要|来|再来|我要|我想要|给我|给我来|帮我来)?{number__1}{product__1}{number__2}{product__2}{number__3}{product__3}{number__4}{product__4}{product__5}(要|我要){size__1}{coldorhot__1}{product__6}(要|我要){size__2}{coldorhot__2}{product__7}(要|我要){size__3}{coldorhot__3}{product__8}(要|我要){size__4}{coldorhot__4}',
            #     keys={'product': ["美式", '拿铁', '奶茶', '咖啡'],
            #           'size': ['大', '小', '大杯', '小杯', '大瓶', '小瓶', '大杯的', '小杯的'],
            #           'coldorhot': ['热的', '冷的', '热', '冷'],
            #           'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶',
            #                      '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶']},
            #     result=[
            #         {'product': 'product__1', 'number': 'number__1', 'size': 'size__1', 'coldorhot': 'coldorhot__1'},
            #         {'product': 'product__2', 'number': 'number__2', 'size': 'size__2', 'coldorhot': 'coldorhot__2'},
            #         {'product': 'product__3', 'number': 'number__3', 'size': 'size__3', 'coldorhot': 'coldorhot__3'},
            #         {'product': 'product__4', 'number': 'number__4', 'size': 'size__4', 'coldorhot': 'coldorhot__4'},
            #     ]
            # ),
            # 奶茶要冷热
            TemplatePares(tempalte='{product__1}(来|我要|要|我想要|给我|给我来|帮我来)?{coldorhot__1}',
                          keys={
                              'product': ["美式", '拿铁', '奶茶', '咖啡'],
                              'coldorhot': ['热的', '冷的','热','冷'],
                          },
                          result=[
                              {'product': '0', 'coldorhot': 'coldorhot__1'},
                          ]
                          ),
            # 拿铁要大杯的
            TemplatePares(tempalte='{product__1}(来|我要|要|我想要喝|给我来|帮我来)?{size__1}',
                          keys={
                              'product': ["美式", '拿铁', '奶茶', '咖啡'],
                              'size': ['大的', '大杯', '大杯的', '小的', '小杯', '小杯的'],
                          },
                          result=[
                              {'product': '0', 'size': 'size__1'},
                          ]
                          ),

            # 冷热
            TemplatePares(tempalte='(来|我要|要|我想要|给我来|帮我来)?{coldorhot__1}',
                          keys={
                                'coldorhot': ['热的', '冷的','热','冷'],
                                },
                          result=[
                              {'product': '0', 'coldorhot': 'coldorhot__1'},
                          ]
                          ),

            # 修改一个订单
            TemplatePares(tempalte='{size__1}(换成){size__2}',
                          keys={
                              'size': ['大的', '大杯', '大杯的', '小的', '小杯', '小杯的'],
                          },
                          result=[
                              {'size': 'size__2', 'upd': ''},
                          ]
                          ),
            # 修改一个订单
            TemplatePares(tempalte='{product__1}(换成){size__2}',
                          keys={
                              'product': ["美式", '拿铁', '奶茶', '咖啡'],
                              'size': ['大的', '大杯', '大杯的', '小的', '小杯', '小杯的'],
                          },
                          result=[
                              {'size': 'size__2', 'upd': ''},
                          ]
                          ),

            # 大小
            TemplatePares(tempalte='(来|我要|要|我想要喝|给我来|帮我来)?{size__1}',
                          keys={
                              'size': ['大的', '大杯', '大杯的', '小的', '小杯', '小杯的'],
                          },
                          result=[
                              {'product': '0', 'size': 'size__1'},
                          ]
                          ),

            # 添加一个订单
            TemplatePares(tempalte='(再要|再来|再给我|帮我再来){number__1}{product__1}(吧)?',
                          keys={
                              'product': ["美式", '拿铁', '奶茶', '咖啡'],
                              'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶',
                                         '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶'],

                          },
                          result=[
                              {'product': 'product__1', 'number': 'number__1'},
                          ]
                          ),

            # 删除一个订单
            TemplatePares(tempalte='{product__1}(我)?(也)?(不要了)',
                          keys={
                              'product': ["美式", '拿铁', '奶茶', '咖啡'],
                          },
                          result=[
                              {'product': 'product__1', 'del': ''},
                          ]
                          ),

            # 删除一个订单
            TemplatePares(tempalte='(我)?(也)?(不要了)',
                          keys={
                              'product': ["美式", '拿铁', '奶茶', '咖啡'],
                          },
                          result=[
                              {'product': '', 'del': ''},
                          ]
                          ),

            # 删除一个订单
            TemplatePares(tempalte='(我不要){product__1}(了)',
                          keys={
                              'product': ["美式", '拿铁', '奶茶', '咖啡'],
                          },
                          result=[
                              {'product': 'product__1', 'del': ''},
                          ]
                          ),

            # 我要一杯水一瓶雪碧一瓶可乐
            # TemplatePares(
            #     tempalte='(我要|来)?{number__1}{product__1}{number__2}{product__2}(送到|到){table_num__1}',
            #     keys={'product': ["白开水", '大麦茶', '可乐', '雪碧', '开水', '水', '矿泉水'],
            #           'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶', "四杯",
            #                      '四瓶', '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶', '4瓶', '5瓶', '5杯', '五瓶', '五杯'
            #               , '6杯', '7杯', '8杯', '9杯', '6瓶', '7瓶', '8瓶', '9瓶', '10瓶', '10杯'
            #               , '六杯', '七杯', '八杯', '九杯', '六瓶', '七瓶', '八瓶', '九瓶', '十瓶', '十杯'],
            #           'table_num': ['一号', '二号', '三号', '四号', '一号桌', '二号桌', '三号桌', '四号桌', '1号桌', '2号桌', '3号桌', '4号桌',
            #                         '1号', '2号', '3号',
            #                         '4号', '两号桌', '五号桌', '六号桌', '七号桌', '八号桌', '九号桌', '十号桌', '5号桌', '6号桌', '7号桌', '8号桌',
            #                         '9号桌', '10号桌',
            #                         '五号', '六号', '七号', '八号', '九号', '十号', '5号', '6号', '7号',
            #                         '8号', '9号', '10号']},
            #     result=[
            #         {'product': 'product__1', 'number': 'number__1', 'table_num': 'table_num__1'},
            #         {'product': 'product__2', 'number': 'number__2', 'table_num': 'table_num__1'},
            #     ]
            # ),
            #
            # # 我要一杯水一瓶雪碧一瓶可乐
            # TemplatePares(
            #     tempalte='(我要)?{number__1}{product__1}{number__2}{product__2}{number__3}{product__3}(送到|到){table_num__1}',
            #     keys={'product': ["白开水", '大麦茶', '可乐', '雪碧', '开水', '水', '矿泉水'],
            #           'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶', "四杯",
            #                      '四瓶', '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶', '4瓶', '5瓶', '5杯', '五瓶', '五杯'
            #               , '6杯', '7杯', '8杯', '9杯', '6瓶', '7瓶', '8瓶', '9瓶', '10瓶', '10杯'
            #               , '六杯', '七杯', '八杯', '九杯', '六瓶', '七瓶', '八瓶', '九瓶', '十瓶', '十杯'],
            #           'table_num': ['一号', '二号', '三号', '四号', '一号桌', '二号桌', '三号桌', '四号桌', '1号桌', '2号桌', '3号桌', '4号桌',
            #                         '1号', '2号', '3号',
            #                         '4号', '两号桌', '五号桌', '六号桌', '七号桌', '八号桌', '九号桌', '十号桌', '5号桌', '6号桌', '7号桌', '8号桌',
            #                         '9号桌', '10号桌',
            #                         '五号', '六号', '七号', '八号', '九号', '十号', '5号', '6号', '7号',
            #                         '8号', '9号', '10号']},
            #     result=[
            #         {'product': 'product__1', 'number': 'number__1', 'table_num': 'table_num__1'},
            #         {'product': 'product__2', 'number': 'number__2', 'table_num': 'table_num__1'},
            #         {'product': 'product__3', 'number': 'number__3', 'table_num': 'table_num__1'},
            #     ]
            #     ),
            #
            # # 水两个雪碧一个
            # TemplatePares(tempalte='(来|再来|我要|我想要喝|给我来|点|给我拿)?{product__1}{number__1}',
            #               keys={'product': ["白开水", '大麦茶', '可乐', '雪碧', '开水', '水', '矿泉水'],
            #                     'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶', "四杯",
            #                                '四瓶', '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶', '4瓶', '5瓶', '5杯', '五瓶', '五杯'
            #                         , '6杯', '7杯', '8杯', '9杯', '6瓶', '7瓶', '8瓶', '9瓶', '10瓶', '10杯'
            #                         , '六杯', '七杯', '八杯', '九杯', '六瓶', '七瓶', '八瓶', '九瓶', '十瓶', '十杯']},
            #               result=[
            #                   {'product': 'product__1', 'number': 'number__1'},
            #               ]
            #               ),
            #
            # # 我要喝可乐
            # TemplatePares(tempalte='(来|再来|我要|我想要喝|给我来|点|给我拿|给我|就要|我想喝)?{number__1}{product__1}',
            #               keys={'product': ["白开水", '大麦茶', '可乐', '雪碧', '开水', '水', '矿泉水'],
            #                     'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶', "四杯",
            #                                '四瓶', '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶', '4瓶', '5瓶', '5杯', '五瓶', '五杯'
            #                         , '6杯', '7杯', '8杯', '9杯', '6瓶', '7瓶', '8瓶', '9瓶', '10瓶', '10杯'
            #                         , '六杯', '七杯', '八杯', '九杯', '六瓶', '七瓶', '八瓶', '九瓶', '十瓶', '十杯']},
            #               result=[
            #                   {'product': 'product__1', 'number': 'number__1'},
            #               ]
            #               ),
            #
            # # 我想要大麦茶和可乐
            # TemplatePares(tempalte='(我要喝|我想喝|我要|我想要喝|我想要)?{product__1}(和){product__2}',
            #               keys={'product': ["白开水", '大麦茶', '可乐', '雪碧', '开水', '水', '矿泉水']},
            #               result=[
            #                   {'product': 'product__1'},
            #                   {'product': 'product__2'},
            #               ]
            #               ),
            #
            # # 我要喝可乐
            # TemplatePares(tempalte='(我要喝|我想喝|我要|我想要喝|我想要)?{product__1}',
            #               keys={'product': ["白开水", '大麦茶', '可乐', '雪碧', '开水', '水', '矿泉水']},
            #               result=[
            #                   {'product': 'product__1'},
            #               ]
            #               ),
            #
            # # 来两杯可乐一杯矿泉水
            # TemplatePares(tempalte='(来)?{number__1}{product__1}{number__2}{product__2}',
            #               keys={'product': ["白开水", '大麦茶', '可乐', '雪碧', '开水', '水', '矿泉水'],
            #                     'number': ['一瓶', '两瓶', '一个', '一杯', '一', '两杯', '两个', '瓶', '杯', '个', '三杯', '三瓶', "四杯",
            #                                '四瓶', '1杯', '2杯', '3杯', '4杯', '1瓶', '2瓶', '3瓶', '4瓶', '5瓶', '5杯', '五瓶', '五杯'
            #                         , '6杯', '7杯', '8杯', '9杯', '6瓶', '7瓶', '8瓶', '9瓶', '10瓶', '10杯'
            #                         , '六杯', '七杯', '八杯', '九杯', '六瓶', '七瓶', '八瓶', '九瓶', '十瓶', '十杯']},
            #               result=[
            #                   {'product': 'product__1', 'number': 'number__1'},
            #                   {'product': 'product__2', 'number': 'number__2'},
            #               ]
            #               ),
        ]

    def identify(self, sentence):
        """"""
        res = []
        # 去除sentence的标点符号
        s = re.sub("""[,。？，‘’'"!:]+""", '', sentence)
        for i in range(15):
            s, match_res, end = self.match(s)
            if match_res:
                res.extend(match_res)
            if len(s) == 0:
                break
            if end:
                break
        return res

    def match(self, sentence):
        """"""
        for t in self.temp_list:
            # sentence = sentence.replace('1', '一').replace('2', '两').replace('3', '三')
            # 得到每个规则的result [{'product': '水', 'number': '一杯'}]
            # 规则匹配成功，则删除已经匹配的字段，再继续匹配
            s, match_res = t.cut_match(sentence)
            if match_res:
                for data in match_res:
                    if data.get('number', '') in ['一个', '两个', '1个', '2个']:
                        data['number'] = data['number'].replace('个', '杯')
                    if data.get('number', '') in ['一瓶', '两瓶']:
                        data['number'] = data['number'].replace('瓶', '杯')
                    if data.get('number', '') in ['瓶', '杯', '个']:
                        data['number'] = '一' + data['number']
                    if data.get('number', '') in ['一', '二']:
                        data['number'] = data['number']+'杯'
                    if data.get('size', '') in ['大', '小']:
                        data['size'] = data['size']+'杯的'
                    if data.get('size', '') in ['大杯', '小杯']:
                        data['size'] = data['size']+'的'
                    if data.get('product', '') in ['水']:
                        data['product'] = '开' + data['product']
                    if data.get('product', '') in ['矿泉水', '白开水']:
                        data['product'] = '开水'
                return s, match_res, False
        return sentence, [], True


if __name__ == '__main__':
    result = OrderCoffeeIdentify().identify('大杯的换成小杯的')
    print(result[0].get('size'))
    print(result)
