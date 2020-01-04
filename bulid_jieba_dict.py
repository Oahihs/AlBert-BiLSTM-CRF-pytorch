# encoding=utf-8
from kglv import Kg
import jieba


def 知识实体转化为结巴词典():
    kg=Kg()
    kg.build_dict()

# def jieba_cut(text):
#     file_name="tdata/kg_dict.txt"
#     jieba.load_userdict(file_name) # file_name 为文件类对象或自定义词典的路径
#     print('/'.join(jieba.cut(text)))

# text="柯基犬是个鬼精灵，非常的可爱，也很聪明，"
# jieba_cut(text)

def 构建词典():
    kg=Kg()
    kg.build_ht_dict()

构建词典()