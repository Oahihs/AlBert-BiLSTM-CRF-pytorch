# coding=utf-8
from tqdm import tqdm
import Terry_toolkit as tkit
# from sqlitedict import SqliteDict
import threading
import time
from tqdm import tqdm
import os

"""
知识保存到数据库


"""




class Kg:
    def __init__(self,db="tadta/kg.db"):
        self.db =tkit.Db(dbpath=db)
        self.tdb=tkit.LDB(path="tdata/lvkg.db")
        self.sdir="tdata/search/"
        self.tdb.load("kg")
        self.ss=   tkit.Search()
        self.ss.ix_path=self.sdir
    def add_search(self,word):
        
        
        if os.path.exists(self.sdir):
            pass
        else:
            
            #初始化搜索
            self.ss.init_search()
        # data=[{'title':'www','content':'223这是我们增加搜索的s第武器篇文档，哈哈 ','path':'https://www.osgeo.cn/whoosh/batch.html'}]
        tt=tkit.Text()
        path=tt.md5(word)
        data=[{'title':word,'content':' ','path':path}]
        # data=[{'title':word,'path':path}]
        # print(data)
        self.ss.add(data)
    def search(self,word):
        return self.ss.find_title(word) 
    def build_dict(self):
        """
        将知识库转化为结巴词典
        """
        with  open('tdata/kg_dict.txt','w') as f:
            for key,item in tqdm(self.tdb.get_all()):
                # print(one)
                # yield key,self.tdb.str_dict(item)
                f.write(key+'\n')
    def build_ht_dict(self):
        """
        将知识库转化为HarvestText词典
        """
        tt=tkit.Text()
        tt.load_ht()
        tt.ht_model="tdata/ht_model"
        tt.typed_words()
        words=[]
        for i,one in tqdm(enumerate(self.tdb.get_all())):
            key,item=one
            # print(one)
            # yield key,self.tdb.str_dict(item)
            # f.write(key+'\n')
            words.append(key)
            if i%1000000==0:
                tt.add_words(words)
        tt.add_words(words)


    def build_data(self):
        """
        将知识转化为数据库存储
        """
        file="/mnt/data/dev/tdata/7Lore_triple.csv"
        kg={}
        predicate={}
        # kgdict = SqliteDict('./kg_db.sqlite', autocommit=True)
        # kgdict = SqliteDict('./kg_db.sqlite')
        with open(file) as f:
            for i,line in tqdm(enumerate (f)):
            # process(line) # 
                # print(line.split(", "))
                one=line.split(", ")
                try:
                    c=one[2].strip('\n')
                except:
                    pass
                self.one(one,c)
                # if len(one)==3 and len(c)<20:

                #     p_one=self.db.get(one[0])
                #     if p_one==None:
                #         self.db.add(one[0],{one[1]:[c]})
                #         continue

                #     if p_one.get(one[1])==None:
                #         p_one[one[1]]=[c]
                #     else:
                #         if c in p_one[one[1]]:
                #             pass
                #             continue
                #         else:
                #             p_one[one[1]].append(c)
                #     self.db.add(one[0],p_one)

    def build_data_v2(self):
        """
        将知识转化为数据库存储
        """
        file="/mnt/data/dev/tdata/baike_triples.txt"
        kg={}
        predicate={}
        # kgdict = SqliteDict('./kg_db.sqlite', autocommit=True)
        # kgdict = SqliteDict('./kg_db.sqlite')
        # self.db.db.disable_autocommit()
        with open(file) as f:
            for i,line in tqdm(enumerate (f)):
            # process(line) # 
                # print(line.split(", "))
                # print(line)
                one=line.split("\t")
                try:
                    c=one[2].strip('\n')
                except:
                    pass
                self.one(one,c)
                # # print(one,c)
                # if len(one)==3 and len(c)<20:

                #     p_one=self.db.get(one[0])
                #     if p_one==None:
                #         self.db.add(one[0],{one[1]:[c]})
                #         continue

                #     if p_one.get(one[1])==None:
                #         p_one[one[1]]=[c]
                #     else:
                #         if c in p_one[one[1]]:
                #             pass
                #             continue
                #         else:
                #             p_one[one[1]].append(c)
                #     # print('p_one',p_one)
                #     self.db.add(one[0],p_one)
                #     # if i%10000==0:
                #     #     try:
                #     #         self.db.db.commit()
                #     #         pass
                #     #     except:
                #     #         pass
                #     # if i%1000000==0:
                #     #     self.db.reload()
                # # try:
                # #     self.db.db.commit()
                # #     pass
                # # except:
                # #     pass
    def get(self,word):
        """
        搜索
         """
        try:
            return self.tdb.str_dict(self.tdb.get(word))
        except:
            # print(222)
            return None

    def test(self):
        try:
            self.tdb.get("额哦哦")
        except:
            print(222)
            # print(self.tdb.get("额哦哦"))
        # for k,v in self.tdb.get_all():
        #     print(k,self.tdb.str_dict(v))
    def one(self,one,c):
        """
        保存一条数据
        """
        # print(one,c)
        if len(one)==3 and len(c)<100:

            # p_one=self.db.get(one[0])
            # 加载数据
            try:
                p_one=self.tdb.str_dict(self.tdb.get(one[0]))
            except:
                p_one={one[1]:[c]}
                # print(one[0],p_one)
                self.tdb.put(one[0],p_one)
                return
                # continue
            # print(one)
            # print(p_one.get(one[1]))

            if p_one.get(one[1])==None:
                p_one[one[1]]={c:{'weight':0,'items':[]}}
            elif type(p_one[one[1]])==list:
                # self.tdb.delete(one[1])
                del p_one[one[1]]
            elif  p_one.get(one[1]).get(c)==None:
                p_one[one[1]][c]={'weight':0,'items':[]}
            else:
                pass
            # print(p_one)
            self.tdb.put(one[0],p_one)
        else:
            print(one)
            print( len(one))
    def build_data_v3(self):
        """
        将知识转化为数据库存储
        使用lv数据库
        """
        file="/mnt/data/dev/tdata/baike_triples.txt"
        kg={}
        predicate={}

        with open(file) as f:
            for i,line in tqdm(enumerate (f)):
            # process(line) # 
                # print(line.split(", "))
                # print(line)
                one=line.split("\t")
                try:
                    c=one[2].strip('\n')
                except:
                    pass
                self.one(one,c)
    def rebuild_data(self):
        """
        格式重新转化

        """
        for key,item in tqdm(self.kg_all()):
            # print(key,self.get(key))
            root={}
            # print(type())
            k=self.tdb.str_dict(self.tdb.get(key))
            if k==None:
                continue
            for p in k.keys():
                # print(p)
                root[p]={}
                if len(k[p])>=1 and type(k[p])==list:
                    for it in k[p]:
                        root[p][it]={'weight':0,'items':[]}
                else:
                    root[p][k[p]]={'weight':0,'items':[]}

            # print(root)
            self.tdb.put(key,root)    

                # p
            # kg.add_search(key)                    
    def kg_all(self):
        # kgdict = 
        #可遍历数据
        return self.tdb.get_all()
        # for key, value in self.tdb.get_all():
        #     yield bytes.decode(key), self.tdb.str_dict(value)
            # print()
    def one_v2(self,one,c):
        # print(one,c)
        if len(one)==3 and len(c)<40:

            # p_one=self.db.get(one[0])
            # 加载数据
            try:
                p_one=self.tdb.str_dict(self.tdb.get(one[0]))
            except:
                p_one={one[1]:[c]}
                # print(one[0],p_one)
                self.tdb.put(one[0],p_one)
                return
                # continue


            if p_one.get(one[1])==None:
                p_one[one[1]]=[c]
            else:
                if c in p_one[one[1]]:
                    pass
                    # continue
                    return
                else:
                    p_one[one[1]].append(c)
            # 保存数据
            # print(one[0],p_one)
            self.tdb.put(one[0],p_one)   
    def kg(self,word):
        return self.db.get(word)
    # word="别让他进来"
    # print(kg(word))
    def kg_list(self,word):
        """
        知识获取
        """
        output=[]
        kg=self.kg(word)
        # print(kg)
        if kg==None:
            return output
        else:
            for b in kg.keys():
                for c in kg[b]:
                    output.append((word,b,c))
            return output

    # print(kg_list(word))


    def build_predicate(self):
        """
     构建关系词   
        """
        file="/mnt/data/dev/tdata/7Lore_triple.csv"
        # kg={}
        limit=10
        with open(file) as f:
            predicate={}
            for i,line in tqdm(enumerate (f)):
            # process(line) # 
                # print(line.split(", "))
                one=line.split(", ")
                # print(len(one))
                # print(one)
                if len(one)==3:
                    if predicate.get(one[1])==None:
                        p=0
                    else:
                        p=predicate.get(one[1])
                    # print('p',p)
                    try:
                        predicate[one[1]]=p+1
                    except:
                        # print(one[1])
                        pass
                    # print(predicate[one[1]])

            # print(predicate)
            # print(len(predicate))
            new_predicate={}
            for w in predicate.keys():
                if predicate[w]>limit:
                    new_predicate[w]=predicate[w]
            # print(len(new_predicate))
            pk=tkit.Pkl(task="predicate")
            pk.save([new_predicate])
    def predicate(self,word):
        """
        获取关系词
        """
        pk=tkit.Pkl(task="predicate")
        data=pk.load()
        for it in data:
            # print(it)
            return it[0].get(word)

    # build_predicate()
    # word="包含类别"
    # print(predicate(word))


def 转化为lv数据库():
    tdb=tkit.LDB(path="tdata/lvkg.db")
    tdb.load("kg")
    # kg=Kg("/mnt/data/dev/github/标注数据/Bert-BiLSTM-CRF-pytorch/tdata/kg.db'")
    db =tkit.Db(dbpath='/mnt/data/dev/github/标注数据/Bert-BiLSTM-CRF-pytorch/tdata/kg.db')
    data=[]
    i=0
    # for i, item in enumerate(db.db):
    for item in tqdm(db.get_all()):
            # print( key,db.get(key))
        
        key,value=item
        # print(key,db.get(key))
        if  type(key)==str:
            new_key=key.strip("']").strip("['")
        new_value=db.get(key)
        if new_value==None:
            pass
        elif type(new_key)==str:
           data.append((new_key,new_value))
        
        try:
            db.delete(key)
        except:
            pass
        
        if i%100000==0:
            # print("***********",i/100000)
            tdb.put_data(data)
            data=[]
        # if i%10000000==0 and i!=0:
        #     db.db.close()
        #     db =tkit.Db(dbpath='/mnt/data/dev/github/标注数据/Bert-BiLSTM-CRF-pytorch/tdata/kg.db')
        i=i+1
    tdb.put_data(data)





def 转化为lv数据库one():
    tdb=tkit.LDB(path="tdata/lvkg.db")
    tdb.load("kg")
    # kg=Kg("/mnt/data/dev/github/标注数据/Bert-BiLSTM-CRF-pytorch/tdata/kg.db'")
    db =tkit.Db(dbpath='/mnt/data/dev/github/标注数据/Bert-BiLSTM-CRF-pytorch/tdata/kg.db')
    data=[]
    i=0
    failed=0
    s=0
    # for i, item in enumerate(db.db):
    for item in tqdm(db.get_all()):
            # print( key,db.get(key))
        i=i+1
        key,value=item
        # print(key,db.get(key))
        if  type(key)==str:
            new_key=key.strip("']").strip("['")
        new_value=db.get(key)
        if new_value==None:
            continue
            pass
        elif type(new_key)==str:
            # print(new_value)
            # print( new_value.get("中文名"))
            if new_value.get("中文名")==None:
                tdb.put(new_key,new_value)
                s=s+1
            elif len(new_value)==1 and new_value.get("中文名")[0]==new_key:
                pass
            elif len(new_value)>=1:
                tdb.put(new_key,new_value)
                s=s+1
                # print(new_key,new_value) 
        try:
            db.delete(key)
        except:
            # print("delete failed")
            failed=failed+1
            pass
        if i%1000000==0 and i!=0:
            # print("***********",i/500000)
            print("failed:",failed)
            print("total:",s)
            return
            # db.db.close()
            # # del db        
            # db =tkit.Db(dbpath='/mnt/data/dev/github/标注数据/Bert-BiLSTM-CRF-pytorch/tdata/kg.db')
        #     
        



def 转化为json():
    # tdb=tkit.LDB(path="tdata/lvkg.db")
    # tdb.load("kg")
    # kg=Kg("/mnt/data/dev/github/标注数据/Bert-BiLSTM-CRF-pytorch/tdata/kg.db'")
    db =tkit.Db(dbpath='/mnt/data/dev/github/标注数据/Bert-BiLSTM-CRF-pytorch/tdata/kg.db')
    data=[]
    tjson=tkit.Json(file_path="tdata/kg/kg_0.json")
    # for i, item in enumerate(tqdm(db.db)):
    i=0
    for item in tqdm(db.get_all()):
            # print( key,db.get(key))
        key,value=item
        # print(key,db.get(key))
        if  type(key)==str:
            new_key=key.strip("']").strip("['")
        new_value=db.get(key)
        if new_value==None:
            pass
        elif type(new_key)==str:
        #    tdb.put(new_key,new_value)
            data.append({'key':new_key, 'value':new_value})
    

        if i%100000==0:
            # print("***********",i/100000)
            tjson.save(data)
            data =[]
        if i%1000000==0:
            tjson=tkit.Json(file_path="tdata/kg/kg_"+str(i)+".json")
            

        i=i+1




def replace_one(kg,key,value,se):
    # kg=Kg()
    # new_key=key.replace("['",'').replace("']",'')
    se.acquire()
    new_key=key.strip("']").strip("['")
    # print(key,new_key)
    kg.db.add(new_key,value)
    kg.db.delete(key)
    se.release()



if __name__ == '__main__':

    kg=Kg()

    word="美国" 
    # print(kg.search(word))
    for item in  kg.search(word):
        print(item['title'],kg.get(item['title']))



    # print(kg.ss.all() )
    # for item in kg.ss.all():
    #     print(item)
    # ss.searcher().documents()
    # kg.add_search("柯基犬")


    # #关键词索引
    for key,item in tqdm(kg.kg_all()):
        # print(key,kg.get(key))
        kg.add_search(key)



    # kg.rebuild_data()

    # kg.build_data()
    # kg.build_data_v3()
    # # # 设置允许5个线程同时运行
    # # semaphore = threading.BoundedSemaphore(7)
    # # for key,value in tqdm(kg.kg_all()):
    # #     t = threading.Thread(target=replace_one, args=(kg,key,value,semaphore))
    # #     t.start()    

    # kg.build_data_v2()
    # for i in range(10000):
    #    转化为lv数据库one()
    # 转化为lv数据库one()
    # 转化为lv数据库()
    # 转化为json()




# # # print(len(kg.db.db))


#     kg=Kg()
#     # # 设置允许5个线程同时运行
#     # semaphore = threading.BoundedSemaphore(7)
#     d=[]
#     for key,value in tqdm(kg.kg_all()):
#         # t = threading.Thread(target=replace_one, args=(kg,key,value,semaphore))
#         # t.start()  
#         # d[key]=0
#         if key in d:
#             pass
#         else:
#             d.append(key)
#     print(len(d))
