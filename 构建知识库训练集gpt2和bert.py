# coding=utf-8
import torch
import torch.nn as nn
from torch.autograd import Variable
from config import Config
from model import BERT_LSTM_CRF
import torch.optim as optim
from utils import load_vocab, read_corpus, load_model, save_model,Tjson
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
import random
from tqdm import tqdm
import os
# import fire

def build_dataset(train_file,type="all"):
    """
    百度训练集
    train_file 文件路径
    type="all" 或者mini 
    mini
    """
    tjson=Tjson(file_path=train_file)
    tjson_save=Tjson(file_path="data/train.json")
    dev_json_save=Tjson(file_path="data/dev.json")
    data=[]
    for item in tqdm(tjson.load()):
        
        text= item['text']
        # print(text)
        # print(item['spo_list'])
        predicate={}
        for n in item['spo_list']:
            predicate[n['predicate']]=[]
        for n in item['spo_list']:
            one={
                "subject":n['subject'],"object":n['object'],
            }
            predicate[n['predicate']].append(one)
        # print(predicate)
        p_n=list(range(20))
        # random.shuffle(p_n)   
        label = ["O"]*len(text)
        for i,p in enumerate( predicate):
            # print('p',p)
            # print(predicate)
            # i=0
            i=0
            # for m in predicate[p]:
            #     start_a =text.find(m['subject'])
            #     end_a=text.find(m['subject'])+len(m['subject'])
            #     for n in range(start_a,end_a):
            #         # label[n]='M_A_'+str(p_n[i])
            #         label[n]='M_A'
            #         pass
            #     start_a =text.find(m['object'])
            #     end_a=text.find(m['object'])+len(m['object'])
            #     for n in range(start_a,end_a):
            #         # label[n]='M_B_'+str(p_n[i])
            #         label[n]='M_A'
            #         pass
            start_p =text.find(p)
            end_p=text.find(p)+len(p)
            if start_p>=0:
                for n in range(start_p,end_p):
                    # label[n]='M_P_'+str(p_n[i])
                    label[n]='M_P'
                    pass
        # print(label)
        if len(list(text))==len(list(label)):
            one={"text":list(text), "label":label}
            data.append(one)
        else:
            # print("pass")
            pass
    if type=="all":
        pass
    elif type=="mini":
        data=data[:200]

    f=int(len(data)*0.85)
    tjson_save.save(data=data[:f])
    dev_json_save.save(data=data[f:])
def auto_label(label,new):
    if label=="O":
        return new
    else:
        # return label+'_'+new
        return new
def mark_word_label(text,label_b,word,tp="实体"):
    p=word
    start_p =text.find(p)
    end_p=text.find(p)+len(p)-1
    if start_p>=0:
        if len(p)>3:
            label_b[start_p]=auto_label(label_b[start_p],'B-'+tp)
            label_b[end_p]=auto_label(label_b[end_p],'E-'+tp)
            for n in range(start_p+1,end_p):
                label_b[n]=auto_label(label_b[n],'M-'+tp)
                pass
        elif len(p)==3:
            label_b[start_p]=auto_label(label_b[start_p],'B-'+tp)
            label_b[end_p]=  auto_label(label_b[end_p],'E-'+tp)
            label_b[start_p+1]=  auto_label(label_b[start_p+1],'M-'+tp)
        elif len(p)==1:
            label_b[start_p]=auto_label(label_b[start_p],'S-'+tp)
        elif len(p)==2:
            label_b[start_p]=auto_label(label_b[start_p],'B-'+tp)
            label_b[end_p]=  auto_label(label_b[end_p],'E-'+tp)
    return label_b
# def mark_one(text,kgs):
#     # root_label = ["O"]*len(text)
#     print("###"*20)
#     print(text)
#     print("kgs",kgs)
#     for ner in kgs.keys():
#         label= ["O"]*len(text)
#         label1=mark_word_label(text,label,ner,"实体")
#         print('word',ner,"++++++++++++++++++++")
#         for pword in kgs[ner]:
#             # kgs[ner][pword]['label']=label1  
            
#             # label1=kgs[ner][pword]['label']
#             # #标记关系
#             # label1=mark_word_label(text,label,ner,"实体")
#             label2=mark_word_label(text,label1,pword,"关系")
#             # print(label2)
#             # print('label1',label1)
#             # # print("---"*10)
#             # print('label2',label2)
#             # kgs[ner][pword]['label']=label2
#             label3=label2
#             # print("-_-"*10)
#             # print("kgs",kgs)
#             for p in kgs[ner][pword]['objects']:
#                 # 标记描述  
#                 label3=mark_word_label(text,label3,p,"描述")
#             # print(ner,pword,kgs[ner][pword]['objects'])
#             kgs[ner][pword]['label']=label3
#             # print('label3',label3)
#             print("￥￥￥￥￥￥￥￥"*20)
#             print(ner,pword,kgs[ner][pword])
#         #     del label3
#         # del label2
#     print(kgs)    


def build_dataset_kg(train_file,type="all"):
    """
    百度训练集
    转化为标注数据集
    train_file 文件路径
    type="all" 或者mini 
    mini

    构建数据思路
    多个描述合并到一个训练里

    使用ner提取出句子中的实体

    文本: ner+句子
    label: ['K']*len(ner)+正常标记
    """
    tjson=Tjson(file_path=train_file)
    all_save=Tjson(file_path="data/train_all.json")
    tjson_save=Tjson(file_path="data/train.json")
    dev_json_save=Tjson(file_path="data/dev.json")
    data=[]
    i=0
    for item in tqdm(tjson.load()):
        # i=i+1
        # if i==1000:
        #     break
        # print(item)
        text= item['text']
     
        # print(text)
        # print(item['spo_list'])
        predicate={}
        for n in item['spo_list']:
            predicate[n['predicate']]=[]
        kgs={}
        for n in item['spo_list']:
            if kgs.get(n['subject'])==None:
                kgs[n['subject']]={}

                label= ["O"]*len(text)
                w=n['subject']
                label=mark_word_label(text,label,w,"实体")

                w=n['predicate']
                label=mark_word_label(text,label,w,"关系")

                w=n['object']
                label=mark_word_label(text,label,w,"描述")

                kgs[n['subject']][n['predicate']]={"objects":[n['object']],'label':label}
            elif  kgs[n['subject']].get(n['predicate'])==None:

                label= ["O"]*len(text)
                w=n['subject']
                label=mark_word_label(text,label,w,"实体")

                w=n['predicate']
                label=mark_word_label(text,label,w,"关系")

                w=n['object']
                label=mark_word_label(text,label,w,"描述")

                kgs[n['subject']][n['predicate']]={"objects":[n['object']],'label':label}
            else:

                label= kgs[n['subject']][n['predicate']]['label']
                w=n['subject']
                label=mark_word_label(text,label,w,"实体")

                w=n['predicate']
                label=mark_word_label(text,label,w,"关系")

                w=n['object']
                label=mark_word_label(text,label,w,"描述")
                kgs[n['subject']][n['predicate']]['objects'].append(n['object'])
        
        # mark_one(text,kgs)
        # print(kgs)
        for ner in kgs.keys():
            for p in kgs[ner]:
                # print('####'*20)
                # print(kgs[ner][p])
                # print(text)
                # print(kgs[ner][p]['label'])
                one={"text":list(ner+'#'+p+'#'+text),'label':len(ner)*['K']+['X']+len(p)*['P']+['X']+kgs[ner][p]['label']}
                if len(one['text'])==len(one['label']):
                    data.append(one)
    if type=="all":
        pass
    elif type=="mini":
        data=data[:200]
    all_save.save(data)
    f=int(len(data)*0.85)
    tjson_save.save(data=data[:f])
    dev_json_save.save(data=data[f:])

def build_dataset_gpt2(train_file,type="all"):
    """
    百度训练集
    train_file 文件路径
    type="all" 或者mini 
    mini
    """
    tjson=Tjson(file_path=train_file)
    tjson_save=Tjson(file_path="data/train.json")
    dev_json_save=Tjson(file_path="data/dev.json")
    data=[]
    f = open('data/gpt2kg.txt','a')
    for item in tqdm(tjson.load()):
        
        text= item['text']
        # print(text)
        # print(item['spo_list'])
        predicate={}
        kg=" [KGS] "
        for n in item['spo_list']:
            # predicate[n['predicate']]=[]
            # print(n)
            # print(n)
            kg=kg+' [KG] '+n['subject']+","+n['predicate']+","+n['object']+" [/KG] "


            pass
        
        # data=text+str(item['spo_list'])
        data=text+kg+" [KGE] "
        print("***"*10)
        print(data)
        f.write(data+'\n\n')
    f.close()


if __name__ == '__main__':
    # fire.Fire()
    train_files=["/mnt/data/dev/tdata/知识提取/train_data.json","/mnt/data/dev/tdata/知识提取/dev_data.json"]
    train_file="data/train.json"
    dev_file="data/dev.json"
    if os.path.exists(train_file) or os.path.exists(dev_file):
        print("文件已经存在")
        print("请手动删除")
    else:
        for f in train_files:
            # build_dataset(f,type="all")
            ###构建知识提取训练集
            build_dataset_kg(f,type="all")
            # build_dataset_gpt2(f,type="mini")










