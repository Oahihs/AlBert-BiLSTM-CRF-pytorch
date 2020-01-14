#encoding=utf-8
from __future__ import unicode_literals
import sys
# sys.path.append("../")
from kglv import Kg
import Terry_toolkit as tkit
import jiagu
from pyltp import Parser
from pyltp import SementicRoleLabeller
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from tqdm import tqdm
import json

import os
class FindKg:
    """
    自动标记知识
    """
    def __init__(self,LTP_DATA_DIR = '/mnt/data/dev/model/ltp/ltp_data_v3.4.0' ):

        self.ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
        self.cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
        self.pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
        self.srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
        self.par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
        self.i=0
        self.tdb=tkit.LDB(path="tdata/lvkg_mark.db")

    def ner(self,text):
        """
        获取ｎｅｒ数据
        """
        segmentor = Segmentor()  # 初始化实例
        segmentor.load(self.cws_model_path)  # 加载模型
        words = segmentor.segment(text)  # 分词
        # print ('\t'.join(words))
        segmentor.release()  # 释放模型

        postagger = Postagger() # 初始化实例
        postagger.load(self.pos_model_path)  # 加载模型

        # words = ['元芳', '你', '怎么', '看']  # 分词结果
        postags = postagger.postag(words)  # 词性标注
        # print("##"*30)
        # print ('\t'.join(postags))
        postagger.release()  # 释放模型

        recognizer = NamedEntityRecognizer() # 初始化实例
        recognizer.load(self.ner_model_path)  # 加载模型
        # words = ['元芳', '你', '怎么', '看']
        # postags = ['nh', 'r', 'r', 'v']
        netags = recognizer.recognize(words, postags)  # 命名实体识别
        recognizer.release()  # 释放模型
        words_list=[]
        for word, flag in zip(words, netags):
            # print(word,flag)
            if flag.startswith("B-"):
                one=[]
                one.append(word)
            elif flag.startswith("I-"):
                one.append(word)
            elif flag.startswith("E-"):
                one.append(word)
                words_list.append("".join(one))
            elif flag.startswith("S-"):
                words_list.append(word)
        # print(words_list)
        # return words_list,words, postags,netags
        return words_list


    def auto_mark(self,text):
        """
        自动标记句子
        """
        # print(ner(text))
        kg=Kg()
        data=[]
        self.kg_tmp=[]
        for word in self.ner(text):
            # print(word)
            # print(kg.get(word))
            kg_one=kg.get(word)
            # print(kg_one)
            if kg_one==None:
                continue
            
            for b in kg_one.keys():
                one_p=[word]
                # print(key)
                # print(text.find(key))
                if  text.find(b)>0:
                    one_p.append(b)
                    # print(one_p)
                    if type(kg_one.get(b))==dict:
                        for c in kg_one.get(b).keys():
                            # print(c)
                            # print(text.find(c))
                            if  text.find(c)>0:
                                # print("222")
                                one_p.append(c) 
                                # print(c)
                            else:
                                one_p=[]
                            # print(one_p)
                            if len(one_p)==3:
                                # 发现一条可标记数据
                                # print("zui",one_p)
                                data.append(one_p)
                else:
                    pass
                self.kg_tmp.append((word,kg_one))
        return data
    def auto_mark_wiki(self,text):
        """
        自动标记wiki句子
        """
        # print(ner(text))
        kg=Kg()
        data=[]
        self.kg_tmp=[]
        self.tdb.load("mark") 
        word=self.keyword
        # print(word)
        # print(kg.get(word))
        tt=tkit.Text()
        knowledge = jiagu.knowledge(text)
        # print(knowledge)
        # for one in  knowledge:
        if len(knowledge)>0:
            key=tt.md5(text+"".join("".join(knowledge)))
            one_item={"text":text,"data":knowledge}
            print("jiagu成功匹配知识",one_item)
            self.tdb.put(key,one_item)
            self.i=self.i+1
        kg_one=kg.get(word)
        # print(kg_one)
        if kg_one==None or text.find(word)<0:
            return data
        print("句子：",text)
        print("发现word",word)
        for b in kg_one.keys():
            one_p=[word]
            # print(key)
            # print(text.find(key))
            if  text.find(b)>0 or b in ["是"]:
                one_p.append(b)
                # print(one_p)
                if type(kg_one.get(b))==dict:
                    for c in kg_one.get(b).keys():
                        # print(c)
                        # print(text.find(c))
                        if  text.find(c)>0:
                            # print("222")
                            one_p.append(c) 
                            # print(c)
                        else:
                            one_p=[]
                        # print(one_p)
                        if len(one_p)==3:
                            # 发现一条可标记数据
                            # print("zui",one_p)

                            data.append(one_p)
            else:
                pass
            self.kg_tmp.append((word,kg_one))
        return data
                                
        
    def one_text(self,text):
        """
        处理一篇文章
        """
        tdb= self.tdb
        tfile=tkit.File()
        tt=tkit.Text()
        # tdb.load("text")
        # text_id=tt.md5(text)
        # try:
        #     tdb.get(text_id)
        #     # continue
        #     return
        # except:
        #     pass
        # sents=tt.sentence_segmentation_v1(text)
        sents=tt.sentence_segmentation(text)
        print("###"*20)
        print("句子：",len(sents))
        tdb.load("mark") 
        for sentence in tqdm(sents):
            # print(sentence)
            # data=self.auto_mark(sentence)
            try:
                data=self.auto_mark_wiki(sentence)
            except:
                pass
            if len(data)>0:
                self.i=self.i+1
                key=tt.md5(sentence+"".join(''.join(data)))
                one={"text":sentence,"data":data}
                # print("知识：",self.kg_tmp)
                print("标记：",one)
                tdb.put(key,one)
                print("###"*20)
                print("已经标记：",self.i)

        # tdb.load("text")
        # tdb.put(text_id,text_id)            

    def bulid_thuocl_dict(self):
        """"
        清华词典"""
        file="/mnt/data/dev/github/Terry-toolkit/Terry-toolkit/Terry_toolkit/resources/THUOCL.json"
        dict_file="tdata/thuocl.txt"
        wikidict=open(dict_file, 'w', encoding = 'utf-8')
        with open(file, 'r', encoding = 'utf-8') as data:
            for it in data:
                # print(it)
                item=json.loads(it)
                # print(item)
                for t in item.keys():
                    wikidict.write("\n".join(item[t]))
                    wikidict.write("\n")
        wikidict.close()
    def bulid_wiki_dict(self):
        """
        构建wiki词典
        """
        path="/mnt/data/dev/tdata/wiki_zh"
        dict_file="tdata/wikidict.txt"
        all_data=[]
        print("开始处理文本")

        # for line in tqdm( tfile.file_List(path, type='txt')):
        #     text=  tfile.open_file(line)
        #     self.one_text(text)
    
        tfile=tkit.File()
        tt=tkit.Text()
        flist=tfile.all_path(dirname=path)

        
        wikidict=open(dict_file, 'w', encoding = 'utf-8')
        i=0
        for file in  tqdm(flist):
            try:
                print(file)
                with open(file, 'r', encoding = 'utf-8') as data:
                    for it in data:
                        i=i+1
                        # print(it)
                        item=json.loads(it[:-1])

                        # print("关键词",item['title'])
                        wikidict.write(item['title'])
                        wikidict.write("\n")
   
            except:
                pass
        wikidict.close()
    def run(self):
        path="/mnt/data/dev/tdata/wiki_zh"
        all_data=[]
        print("开始处理文本")

        # for line in tqdm( tfile.file_List(path, type='txt')):
        #     text=  tfile.open_file(line)
        #     self.one_text(text)
    
        tfile=tkit.File()
        tt=tkit.Text()
        flist=tfile.all_path(dirname=path)
        # print("flist",flist)
  
        i=0
        for file in  flist:
            try:
                print(file)
                with open(file, 'r', encoding = 'utf-8') as data:
                    for it in data:
                        i=i+1
                        # print(it)
                        item=json.loads(it[:-1])
                        # print(item)
                        text=item['title']+"\n"+item['text']
                        print("关键词",item['title'])
                        print("已经标记：",self.i)
                        self.keyword=item['title']
                        self.one_text(item['text'])
                    
            except:
                pass


# FindKg().run()

# 构建wiki词典
# FindKg().bulid_wiki_dict()
FindKg().bulid_thuocl_dict()

# text="""'夸奥蒂特兰是墨西哥的城市，由墨西哥州负责管辖，位于该国南部，面积42平方公里，海拔高度2,250米，主要经济活动有工业和商业，2010年人口1450万人"""
# data=FindKg().auto_mark(text)
# print(data)





























 


content1 = """环境很好，位置独立性很强，比较安静很切合店名，半闲居，偷得半日闲。点了比较经典的菜品，味道果然不错！烤乳鸽，超级赞赞赞，脆皮焦香，肉质细嫩，超好吃。艇仔粥料很足，香葱自己添加，很贴心。金钱肚味道不错，不过没有在广州吃的烂，牙口不好的慎点。凤爪很火候很好，推荐。最惊艳的是长寿菜，菜料十足，很新鲜，清淡又不乏味道，而且没有添加调料的味道，搭配的非常不错！"""
content2 = """近日，一条男子高铁吃泡面被女乘客怒怼的视频引发热议。女子情绪激动，言辞激烈，大声斥责该乘客，称高铁上有规定不能吃泡面，质问其“有公德心吗”“没素质”。视频曝光后，该女子回应称，因自己的孩子对泡面过敏，曾跟这名男子沟通过，但对方执意不听，她才发泄不满，并称男子拍视频上传已侵犯了她的隐私权和名誉权，将采取法律手段。12306客服人员表示，高铁、动车上一般不卖泡面，但没有规定高铁、动车上不能吃泡面。
            高铁属于密封性较强的空间，每名乘客都有维护高铁内秩序，不破坏该空间内空气质量的义务。这也是乘客作为公民应当具备的基本品质。但是，在高铁没有明确禁止食用泡面等食物的背景下，以影响自己或孩子为由阻挠他人食用某种食品并厉声斥责，恐怕也超出了权利边界。当人们在公共场所活动时，不宜过分干涉他人权利，这样才能构建和谐美好的公共秩序。
            一般来说，个人的权利便是他人的义务，任何人不得随意侵犯他人权利，这是每个公民得以正常工作、生活的基本条件。如果权利可以被肆意侵犯而得不到救济，社会将无法运转，人们也没有幸福可言。如西谚所说，“你的权利止于我的鼻尖”，“你可以唱歌，但不能在午夜破坏我的美梦”。无论何种权利，其能够得以行使的前提是不影响他人正常生活，不违反公共利益和公序良俗。超越了这个边界，权利便不再为权利，也就不再受到保护。
            在“男子高铁吃泡面被怒怼”事件中，初一看，吃泡面男子可能侵犯公共场所秩序，被怒怼乃咎由自取，其实不尽然。虽然高铁属于封闭空间，但与禁止食用刺激性食品的地铁不同，高铁运营方虽然不建议食用泡面等刺激性食品，但并未作出禁止性规定。由此可见，即使食用泡面、榴莲、麻辣烫等食物可能产生刺激性味道，让他人不适，但是否食用该食品，依然取决于个人喜好，他人无权随意干涉乃至横加斥责。这也是此事件披露后，很多网友并未一边倒地批评食用泡面的男子，反而认为女乘客不该高声喧哗。
            现代社会，公民的义务一般分为法律义务和道德义务。如果某个行为被确定为法律义务，行为人必须遵守，一旦违反，无论是受害人抑或旁观群众，均有权制止、投诉、举报。违法者既会受到应有惩戒，也会受到道德谴责，积极制止者则属于应受鼓励的见义勇为。如果有人违反道德义务，则应受到道德和舆论谴责，并有可能被追究法律责任。如在公共场所随地吐痰、乱扔垃圾、脱掉鞋子、随意插队等。此时，如果行为人对他人的劝阻置之不理甚至行凶报复，无疑要受到严厉惩戒。
            当然，随着社会的发展，某些道德义务可能上升为法律义务。如之前，很多人对公共场所吸烟不以为然，烟民可以旁若无人地吞云吐雾。现在，要是还有人不识时务地在公共场所吸烟，必然将成为众矢之的。
            再回到“高铁吃泡面”事件，要是随着人们观念的更新，在高铁上不得吃泡面等可能产生刺激性气味的食物逐渐成为共识，或者上升到道德义务或法律义务。斥责、制止他人吃泡面将理直气壮，否则很难摆脱“矫情”，“将自我权利凌驾于他人权利之上”的嫌疑。
            在相关部门并未禁止在高铁上吃泡面的背景下，吃不吃泡面系个人权利或者个人私德，是不违反公共利益的个人正常生活的一部分。如果认为他人吃泡面让自己不适，最好是请求他人配合并加以感谢，而非站在道德制高点强制干预。只有每个人行使权利时不逾越边界，与他人沟通时好好说话，不过分自我地将幸福和舒适凌驾于他人之上，人与人之间才更趋于平等，公共生活才更趋向美好有序。"""
content3 = '''（原标题：央视独家采访：陕西榆林产妇坠楼事件在场人员还原事情经过）
央视新闻客户端11月24日消息，2017年8月31日晚，在陕西省榆林市第一医院绥德院区，产妇马茸茸在待产时，从医院五楼坠亡。事发后，医院方面表示，由于家属多次拒绝剖宫产，最终导致产妇难忍疼痛跳楼。但是产妇家属却声称，曾向医生多次提出剖宫产被拒绝。
事情经过究竟如何，曾引起舆论纷纷，而随着时间的推移，更多的反思也留给了我们，只有解决了这起事件中暴露出的一些问题，比如患者的医疗选择权，人们对剖宫产和顺产的认识问题等，这样的悲剧才不会再次发生。央视记者找到了等待产妇的家属，主治医生，病区主任，以及当时的两位助产师，一位实习医生，希望通过他们的讲述，更准确地还原事情经过。
产妇待产时坠亡，事件有何疑点。公安机关经过调查，排除他杀可能，初步认定马茸茸为跳楼自杀身亡。马茸茸为何会在医院待产期间跳楼身亡，这让所有人的目光都聚焦到了榆林第一医院，这家在当地人心目中数一数二的大医院。
就这起事件来说，如何保障患者和家属的知情权，如何让患者和医生能够多一份实质化的沟通？这就需要与之相关的法律法规更加的细化、人性化并且充满温度。用这种温度来消除孕妇对未知的恐惧，来保障医患双方的权益，迎接新生儿平安健康地来到这个世界。'''
content4 = '李克强总理今天来我家了,我感到非常荣幸'
content5 = ''' 以色列国防军20日对加沙地带实施轰炸，造成3名巴勒斯坦武装人员死亡。此外，巴勒斯坦人与以色列士兵当天在加沙地带与以交界地区发生冲突，一名巴勒斯坦人被打死。当天的冲突还造成210名巴勒斯坦人受伤。
当天，数千名巴勒斯坦人在加沙地带边境地区继续“回归大游行”抗议活动。部分示威者燃烧轮胎，并向以军投掷石块、燃烧瓶等，驻守边境的以军士兵向示威人群发射催泪瓦斯并开枪射击。'''






content2="""

北极星节能环保网讯:“十三五”环保大幕已经开启，村镇水环境治理作为环保的重中之重，已引起全社会多方关注，行业发展潜力巨大，市场前景广阔。2016年9月22-23日，由中国国际贸易促进委员会建设行业分会、住建部农村污水处理技术北方研究中心主办，《水工业市场》杂志承办的第六届中国农村和小城镇水环境治理论坛在北京新疆大厦隆重举办。村镇水环境领域众多专家与企业大咖围绕村镇水环境治理产业政策、适用技术、市场焦点等问题精彩“论道”。中国人民大学环境学院副院长王洪臣围绕“中国农村污水治理技术瓶颈及对策”发表了主题演讲，《水工业市场》杂志编辑整理了他的演讲内容，期望提供有益借鉴。 1、污水分散治理与农村污水处理的关系污水分散治理指的是小股污水的治理，也就是我们通常看到的高速公路服务站、度假村、远离城区的机构、一些不能接入管网的企业，还有远离市政集中处理设施的居住区(中国农村;西方社区)，使用就地原位收集处理的污水处理系统。西方的农村几十年前就完成了城镇化，在西方语境中现在没有“农村污水处理”这个词，西方叫“乡村地区的污水处理”。西方污水分散治理主要的任务是在社区，但中国有很多农村，中国污水分散治理主要的任务在农村。在西方，通常是有钱人在社区住。这些社区的市政基础设施的标准和管理的水平比城市还要高。再者，在居住空间上，西方人更加注重私密性，处于散住的状态，户与户之间都有土地，相隔几十米。像美国25%的人不住在城里，住在社区，也就是所谓的乡村地区，但他们不是农民。美国社区的污水处理分以下五类建设管理体制，前四类为集中建设，其余为原位建设。(1)管理实体所有制：适用于高环境敏感度且对出水水质要求严格的地区。与管理实体运行维护制不同的是，管理实体拥有分散处理设施，并且对分散处理设施的规划、管理、运行、维护全面负责。(2)管理实体运行维护制：适用于建有许多分散处理装置的高环境敏感度(饮用水源地)的地区，为了达到水质要求，必须保证频繁而可靠的运行和维护。与运行许可制不同，政府将运行许可证颁发给管理实体而非设施所有者，以保证运行的效果。(3)运行许可制：适用于需要持续保持出水水质的地区，政府将一定期限的运行许可证颁发给设施的所有者，若设施运行情况良好，许可证的年限可以延长。为了达到出水标准，设施的所有者应雇佣专业的维护和运行者。(4)维护合同制：通常用在稍微复杂一些的处理系统，比如需要进行预处理的系统。这种模式下，业主需通过合同雇佣专业的操作人员来完成必要的维护工作。(5)业主自觉制：最低层次的管理，适合用于周围没有饮用水源或地下水埋藏较深的低环境敏感区域、私人拥有和运行的污水处理系统。和西方不同，中国农村是群居社会，在北方户与户之间只隔一堵墙，在南方户与户之间只隔很短的一段距离，这为我们解决农村污水治理问题降低了难度。从成本方面考虑，农村污水处理设施可以全部集中建设。但中国共有270万个自然村，60万个行政村，粗略估计只建成了5000多座城镇污水处理设施。而美国已全部建设了社区集中处理设施，共13950座，相当于中国13950个村庄的设施数量;日本已建成75%的社区集中处理设施，共3600座， 相当于中国3600 个村庄的设施数量(见图1)。




"""






def get_triples(content):
    tdict={}
    extractor = tkit.TripleExtractor()
    svos = extractor.triples_main(content)
    # print('svos', svos)
    for sentence,items in svos:
        # print(",".join(item))
        
        for item in items:
         
            if len(item)==4 and item[3]=="主谓宾":
                print(item)
            # if len(item)==4:
                if tdict.get(item[0])==None:
                    tdict[item[0]]={item[1]:[(item[2],sentence)]}
                elif tdict[item[0]].get(item[2])==None:
                    tdict[item[0]][item[1]]=[(item[2],sentence)]
                else:
                    tdict[item[0]][item[1]].append((item[2],isentence))
    print(tdict)
    print(tdict.keys())
            




# get_triples(content2)

# def replace_one(text):
#     xdict={0:"赵",1:"孙",2:"李",
#     3:"吴",
#     4:"郑",
#     5:"王",
#     6:"陈",}
#     text=text.replace("小王",xdict[0])
#     return text