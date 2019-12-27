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
    dev_file="data/train.json"
    if os.path.exists(train_file) or os.path.exists(dev_file):
        print("文件已经存在")
        print("请手动删除")
    else:
        for f in train_files:
            # build_dataset(f,type="all")
            build_dataset(f,type="mini")
            # build_dataset_gpt2(f,type="mini")










