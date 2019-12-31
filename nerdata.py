# coding=utf-8
from utils import load_vocab, read_corpus, load_model, save_model,Tjson
from tqdm import tqdm
#         # return ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "[CLS]","[SEP]"]
#         return ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "X","[CLS]","[SEP]"]
import Terry_toolkit as tkit


# def 

# for 

def ner_rebulid():
    """
    将原有数据转化为标记数据
    """
    new_train=Tjson(file_path="data/train.json")
    new_dev=Tjson(file_path="data/dev.json")
    files=["data/o/train.json","data/o/dev.json"]
    data=[]
    for file in files:
        for  line in Tjson(file_path=file).load():
            # print("line",line['label'])
            new_label={}
            for i,label in enumerate(line['label']):
                one={}
                new_label[i]=label
                if i==0:
                    a={'type':"实体",'num':[]}

                if label=="B-ORG":

                    # 在为O时候处理
                    if len(a['num'])>=2:
                        for key,i_n in enumerate(a['num']):
                            if key==0:
                                new_label[i_n]="B-"+a['type']
                            elif key==len(a['num'])-1:
                                new_label[i_n]="E-"+a['type']
                            else:
                                new_label[i_n]="M-"+a['type']
                    elif len(a['num'])==1:
                        new_label[a['num'][0]]="S-"+a['type']
                    a={'type':"实体",'num':[i]}


                elif label=="I-ORG":
                    a['num'].append(i)
                elif label=="B-PER":

                    # 在为O时候处理
                    if len(a['num'])>=2:
                        for key,i_n in enumerate(a['num']):
                            if key==0:
                                new_label[i_n]="B-"+a['type']
                            elif key==len(a['num'])-1:
                                new_label[i_n]="E-"+a['type']
                            else:
                                new_label[i_n]="M-"+a['type']
                    elif len(a['num'])==1:
                        new_label[a['num'][0]]="S-"+a['type']
                    a={'type':"实体",'num':[i]}


                elif label=="I-PER":
                    a['num'].append(i)
                elif label=="B-LOC":
                    # 在为O时候处理
                    if len(a['num'])>=2:
                        for key,i_n in enumerate(a['num']):
                            if key==0:
                                new_label[i_n]="B-"+a['type']
                            elif key==len(a['num'])-1:
                                new_label[i_n]="E-"+a['type']
                            else:
                                new_label[i_n]="M-"+a['type']
                    elif len(a['num'])==1:
                        new_label[a['num'][0]]="S-"+a['type']        
                    a={'type':"地点",'num':[i]}


                elif label=="I-LOC":
                    a['num'].append(i)
                else:
                    # 在为O时候处理
                    if len(a['num'])>=2:
                        for key,i_n in enumerate(a['num']):
                            if key==0:
                                new_label[i_n]="B-"+a['type']
                            elif key==len(a['num'])-1:
                                new_label[i_n]="E-"+a['type']
                            else:
                                new_label[i_n]="M-"+a['type']
                    elif len(a['num'])==1:
                        new_label[a['num'][0]]="S-"+a['type']

                    # a={'type':"实体",'num':[i]}
            labels=[]
            # print(new_label)
            tags={}
            for l in new_label:
                labels.append(new_label[l])
                # print(new_label[l])
                tags[new_label[l]]=0
            if len(tags)>1:
                one={"text":line["text"], "label":labels}
                # print(one)
                data.append(one)
    f=int(len(data)*0.85)
    new_train.save(data[:f])
    new_dev.save(data[f:])



def _read_data( input_file):
    """Reads a BIO data."""
    max_length=100
    # num=max_length #定义每组包含的元素个数
    with open(input_file) as f:
        lines = []
        words = []
        labels = []
        stop = ["。","!","！"]
        for line in f:
            contends = line.strip()
            
            # print(len(line.strip().split(' ')))
            word = line.strip().split(' ')[0]
            label = line.strip().split(' ')[-1]

            if contends.startswith("-DOCSTART-"):
                words.append('')
                continue
            # if len(contends) == 0 and words[-1] == '。':
            if len(contends) == 0:
                # l = ' '.join([label for label in labels if len(label) > 0])
                # w = ' '.join([word for word in words if len(word) > 0])
                l=[label for label in labels if len(label) > 0]
                w = [word for word in words if len(word) > 0]
                if l==w:
                    # print('xian')
                    pass
                else:
                    w_one=[]
                    l_one=[]
                    # n=0
                    tags={}
                    for i,it in enumerate(w):
                        #基于句子分段
                        if it in stop:
                            w_one.append(w[i])
                            l_one.append(l[i])
                            tags[l[i]]=0
                            # 如果标记内容过少则忽略
                            if len(tags)>1:
                                lines.append([l_one, w_one])
                            tags={}
                            w_one=[]
                            l_one=[]
                        elif i==len(w)-1:
                            if len(tags)>1:
                                lines.append([l_one, w_one])
                            tags={}
                            w_one=[]
                            l_one=[]
                        else:
                            tags[l[i]]=0
                            w_one.append(w[i])
                            l_one.append(l[i])
                    
                    # # 如果内容过长自动分段
                    # if len(l)> max_length:
                    #     for i in range(0,len(l),max_length):
                    #         # print l[i:i+num]
                    #         lines.append([l[i:i+max_length], w[i:i+max_length]])
                    # else:
                    #     lines.append([l, w])
                words = []
                labels = []
                continue
            words.append(word)
            labels.append(label)
        return lines


def build_ner(input_file,tags=None,type='all'):
    d=_read_data(input_file)
    # tjson=Tjson(file_path=train_file)
    tjson_save=Tjson(file_path="data/train.json")
    dev_json_save=Tjson(file_path="data/dev.json")
    data=[]
    if tags==None:
        tags={ "<pad>":1,"O":1,"<start>":1,"<eos>":1}

    for item in tqdm(d):
        
        text= item[0]
        # print(text)
        # print(item['spo_list'])
        # predicate={}
        # for n in item['spo_list']:
        #     predicate[n['predicate']]=[]
    
        # print(label)
        for label in item[0]:
            tags[label]=1
        if len(list(item[0]))==len(list(item[1])):
            one={"text":item[1], "label":item[0]}
            data.append(one)
        else:
            # print("pass")
            pass
    if type=="all":
        pass
    elif type=="mini":
        data=data[:200]
    # print(tags)
    # with open("data/tag.txt","w") as f:
    #     f.write("\n".join(tags.keys()))

    f=int(len(data)*0.85)
    tjson_save.save(data=data[:f])
    dev_json_save.save(data=data[f:])
    return tags

def run(input_files):
    # data=_read_data(input_file)
    # print(data)
    tags=None
    for f in input_files:
        print(f)
        tags=build_ner(f,tags)

    # with open("data/tag.txt","w") as f:
    #     f.write("\n".join(tags.keys()))

# # input_files=["/mnt/data/dev/tdata/ner/dev.txt","/mnt/data/dev/tdata/ner/train.txt",'/mnt/data/dev/tdata/ner/test.txt','/mnt/data/dev/tdata/ner/example.train','/mnt/data/dev/tdata/ner/example.dev','/mnt/data/dev/tdata/ner/example.test','/mnt/data/dev/tdata/ner/dh_msra.txt','/mnt/data/dev/tdata/ner/weiboNER.2.txt','/mnt/data/dev/tdata/ner/weiboNER.1.txt','/mnt/data/dev/tdata/ner/weiboNER.3.txt']


# # input_files=['/mnt/data/dev/github/数据处理工具/tool_data_processing/data/text/日本短尾猫.txt.anns']
# path="/mnt/data/dev/github/数据处理工具/tool_data_processing/data/text/"
# tfile=tkit.File()
# input_files=tfile.file_List( path, type='anns')
# run(input_files)

# 将原始数据转换
# ner_rebulid()


# input_files=['/mnt/data/dev/github/数据处理工具/tool_data_processing/data/text/日本短尾猫.txt.anns']
path="/mnt/data/dev/github/数据处理工具/tool_data_processing/data/text/"
tfile=tkit.File()
input_files=tfile.file_List( path, type='anns')
run(input_files)