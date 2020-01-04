import json
import gzip
from tqdm import tqdm
import threading
import time
from kglv import Kg

"""
将wikidata转化为数据
"""

class TT:
    def __init__(self,num=5):
        self.semaphore = threading.BoundedSemaphore(num)
    def load(self,func,args):
        self.t = threading.Thread(target=func, args=(args,self.semaphore))
        
        pass #
    def start(self):
        self.t.start()
        pass #




def stream_gzipped_lines(file):
    # with gzip.GzipFile(fileobj=file) as gf:
    with gzip.open(file, 'rt') as gf:
        for ln in gf:
            yield ln

def stream_gzipped_json_list(file):
    for i,ln in enumerate( stream_gzipped_lines(file)):
        if ln == b'[\n' or ln == b']\n':
            continue
        # print("##"*30)
        # print(type(ln))
        
        if ln.endswith("\n"):
            yield ln[:-2]
            # print(json.loads(ln[:-2]))

        # if type(ln)==str and ln.endswith(b',\n'): # all but the last element
        #     yield json.loads(ln[:-2])
        # else:
        #     yield json.loads(ln)
        # if i%1000 == 0 and i !=0:
        #     break 
def get(file):
    for obj in stream_gzipped_json_list(file):
        try:
            yield json.loads(obj)
        except:
            pass     
def p_one(line,se):
    se.acquire()
    new_one={}
    for key in line.keys():
        # print(key)
        # print ("同义词",line['aliases']['zh-hans']['value'])
        

        try:
            # print (key,line[key]['zh-hans']['value'])
            new_one[key]=line[key]['zh-hans']['value']
        except:
            pass
    new_one['aliases']=[]
    for a in  line['aliases']:
        try:
            new_one['aliases'].append(a['value'])
        except:
            pass       
    if new_one.get("labels")!=None:
    #    data.append(new_one)
        return new_one
    se.release()  


def data_kg(one):
    """
    添加数据
    """
    kg=Kg()
    kg.one(one,one[2])


def one(line):
    # se.acquire()
    new_one={}
    for key in line.keys():
        # print(key)
        # print ("同义词",line['aliases']['zh-hans']['value'])
        try:
            # print (key,line[key]['zh-hans']['value'])
            new_one[key]=line[key]['zh-hans']['value']
        except:
            pass
    new_one['aliases']=[]
    for a in  line['aliases']:
        try:
            new_one['aliases'].append(a['value'])
        except:
            pass       
    if new_one.get("labels")!=None:
    #    data.append(new_one)
        return new_one
    
    # se.release() 

def one_triple(one):
    """
    转化为三元组
    """
    result=[]
    if one.get("descriptions")!=None:
        result.append((one.get("labels"),"是",one.get("descriptions")))
    for aliase in one.get("aliases"):
        result.append((one.get("aliases"),"又称",one.get("descriptions")))
    return result

file='/mnt/data/dev/tdata/20191230.json.gz'
data=[]
# tt=TT(7)
kg=Kg()
for line in tqdm(get(file)):
    one_line=one(line)
    # print(one_line)
    if one_line!=None:
        triples=one_triple(one_line)
        # print(triples)
        for triple in triples:
            # data_kg(triple)
            kg.one(triple,triple[2])


    # try:
    #     tt.load(p_one,line)
    #     tt.start()
    # except:
    #     pass
     


    # # print (line['claims'])
    # try:
    #     # print ("实体",line['labels']['zh-hans']['value'])
    #     print ("同义词",line['aliases']['zh-hans'])
    #     # print ("介绍",line['descriptions']['zh-hans']['value'])
    #     pass
    # except:
    #     pass
    # print (line)

# # stream_gzipped_json_list(file)

print(len(data))
# print(data)