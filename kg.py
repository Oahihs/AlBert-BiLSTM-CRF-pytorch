# coding=utf-8
from utils import load_vocab, read_corpus, load_model, save_model,Tjson
from tqdm import tqdm
#         # return ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "[CLS]","[SEP]"]
#         return ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "X","[CLS]","[SEP]"]
import Terry_toolkit as tkit
from sqlitedict import SqliteDict
import threading
import time


"""
知识保存到数据库


"""

class Kg:
    def __init__(self,db="kg.db"):
        self.db =tkit.Db(dbpath=db)
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
                if len(one)==3 and len(c)<20:

                    p_one=self.db.get(one[0])
                    if p_one==None:
                        self.db.add(one[0],{one[1]:[c]})
                        continue

                    if p_one.get(one[1])==None:
                        p_one[one[1]]=[c]
                    else:
                        if c in p_one[one[1]]:
                            pass
                            continue
                        else:
                            p_one[one[1]].append(c)
                    self.db.add([one[0]],p_one)

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
                # print(one,c)
                if len(one)==3 and len(c)<20:

                    p_one=self.db.get(one[0])
                    if p_one==None:
                        self.db.add(one[0],{one[1]:[c]})
                        continue

                    if p_one.get(one[1])==None:
                        p_one[one[1]]=[c]
                    else:
                        if c in p_one[one[1]]:
                            pass
                            continue
                        else:
                            p_one[one[1]].append(c)
                    # print('p_one',p_one)
                    self.db.add([one[0]],p_one)
                    # if i%10000==0:
                    #     try:
                    #         self.db.db.commit()
                    #         pass
                    #     except:
                    #         pass
                    # if i%1000000==0:
                    #     self.db.reload()
                # try:
                #     self.db.db.commit()
                #     pass
                # except:
                #     pass
                            
    def kg_all(self):
        # kgdict = 
        #可遍历数据
        for key, value in self.db.db:
            yield key, self.db.get(key)
            # print()

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
        print(kg)
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











# class Kg:
#     def build_data(self):
#         """
#         将知识转化为数据库存储
#         """
#         file="/mnt/data/dev/tdata/7Lore_triple.csv"
#         kg={}
#         predicate={}
#         # kgdict = SqliteDict('./kg_db.sqlite', autocommit=True)
#         kgdict = SqliteDict('./kg_db.sqlite')
#         with open(file) as f:
#             for i,line in tqdm(enumerate (f)):
#             # process(line) # 
#                 # print(line.split(", "))
#                 one=line.split(", ")
#                 try:
#                     c=one[2].strip('\n')
#                 except:
#                     pass
#                 if len(one)==3:
#                     try:
#                         p_one=kgdict[one[0]]
#                     except:
#                         kgdict[one[0]]={one[1]:[c]}
#                         # print("cc")
#                         continue

#                     if p_one.get(one[1])==None:
#                         p_one[one[1]]=[c]
#                     else:
#                         if c in p_one[one[1]]:
#                             pass
#                             continue
#                         else:
#                             p_one[one[1]].append(c)
#                     kgdict[one[0]]=p_one
#                 # print(i)
#                 if i%10000==0:
#                     kgdict.commit()
#             kgdict.commit()
#             kgdict.close() 
                        
                    
#             #         if kg.get(one[0])==None:
#             #             kg[one[0]]={one[1]:[c]}
#             #         elif kg[one[0]].get(one[1])==None:
#             #             kg[one[0]][one[1]]=[c]
#             #         else:
#             #             kg[one[0]][one[1]].append(c)
#             #     # if i>10:
#             #     #     print(kg)
#             #     #     continue
#             # pk=tkit.Pkl(task="kg")
#             # pk.save([kg])        

#     # load_data()
#     # def kg():
#     #     kgdict = SqliteDict('./kg_db.sqlite', autocommit=True)
#     #     for key, value  in kgdict.iteritems():
#     #         print("#####"*30)
#     #         print(key, value  )

#     # kg()
#     def kg_all(self):
#         # kgdict = 
#         #可遍历数据
#         with SqliteDict('./kg_db.sqlite') as d:
#             for key, value in d.iteritems():
#                 yield key, value

#     def kg(self,word):
#         kgdict = SqliteDict('./kg_db.sqlite', autocommit=True)
#         try:
#             return kgdict[word]
#         except:
#             return {}
#     # word="别让他进来"
#     # print(kg(word))
#     def kg_list(self,word):
#         """
#         知识获取
#         """
#         output=[]
#         kg=self.kg(word)
#         for b in kg.keys():
#             for c in kg[b]:
#                 output.append((word,b,c))
#         return output

#     # print(kg_list(word))


#     def build_predicate(self):
#         """
#      构建关系词   
#         """
#         file="/mnt/data/dev/tdata/7Lore_triple.csv"
#         # kg={}
#         limit=10
#         with open(file) as f:
#             predicate={}
#             for i,line in tqdm(enumerate (f)):
#             # process(line) # 
#                 # print(line.split(", "))
#                 one=line.split(", ")
#                 # print(len(one))
#                 # print(one)
#                 if len(one)==3:
#                     if predicate.get(one[1])==None:
#                         p=0
#                     else:
#                         p=predicate.get(one[1])
#                     # print('p',p)
#                     try:
#                         predicate[one[1]]=p+1
#                     except:
#                         # print(one[1])
#                         pass
#                     # print(predicate[one[1]])

#             # print(predicate)
#             # print(len(predicate))
#             new_predicate={}
#             for w in predicate.keys():
#                 if predicate[w]>limit:
#                     new_predicate[w]=predicate[w]
#             # print(len(new_predicate))
#             pk=tkit.Pkl(task="predicate")
#             pk.save([new_predicate])
#     def predicate(self,word):
#         """
#         获取关系词
#         """
#         pk=tkit.Pkl(task="predicate")
#         data=pk.load()
#         for it in data:
#             # print(it)
#             return it[0].get(word)

#     # build_predicate()
#     # word="包含类别"
#     # print(predicate(word))



# kg=Kg()
# #转化
# # kg.build_data()
# l=kg.kg("昆藻茶")
# print(l)

# # kg.kg_all()
# for key,value in tqdm(kg.kg_all()):
    
#     # new_key=key.replace("['",'').replace("']",'')
#     new_key=key.strip("']").strip("['")
#     # print(key,new_key)
#     kg.db.add(new_key,value)
#     kg.db.delete(key)

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
    # # # 设置允许5个线程同时运行
    # # semaphore = threading.BoundedSemaphore(7)
    # # for key,value in tqdm(kg.kg_all()):
    # #     t = threading.Thread(target=replace_one, args=(kg,key,value,semaphore))
    # #     t.start()    

    kg.build_data_v2()




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
