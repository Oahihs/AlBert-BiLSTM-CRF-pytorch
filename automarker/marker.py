# coding=utf-8
import torch
import torch.nn as nn
from torch.autograd import Variable
from config import Config
from model import ALBERT_LSTM_CRF
import torch.optim as optim
from utils import load_vocab, read_corpus, load_model, save_model,build_input,Tjson
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
import fire




class Pre:
    """
    执行预测操作
    content=["柯基犬是个狗子"]
    P=Pre()
    result=P.pre(content)
    print(result)  

    >>>[('柯基犬真是和牛逼', [{'type': '实体', 'words': ['柯', '基', '犬']}])]  
    """
    def __init__(self):
        self.args={
            "load_path":"result/pytorch_model.bin",
            "load_model":True,
            "use_cuda":False,
        }
        
        config = Config()
        config.update_json(self.args)
        self.config=config
        print( self.config)
        self.load_model()

    def load_model(self):
        """
        加载模型
        """

        # config = Config()
        # config.update_json(self.args)
        config=self.config
        # print('当前设置为:\n', config)
        if config.use_cuda:
            torch.cuda.set_device(config.gpu)
        # print('loading corpus')
        vocab = load_vocab(config.vocab)
        label_dic = load_vocab(config.label_file)
        tagset_size = len(label_dic)
        model = ALBERT_LSTM_CRF(config.albert_path, tagset_size, config.albert_embedding, config.rnn_hidden, config.rnn_layer, dropout_ratio=config.dropout_ratio, dropout1=config.dropout1, use_cuda=config.use_cuda)
        if config.load_model:
            assert config.load_path is not None
            # 
            model = load_model(model, name=config.load_path)
        if config.use_cuda:
            model.cuda()
        # return model, vocab, label_dic
        self.model, self.vocab, self.label_dic=model, vocab, label_dic

    def build_input(self,content_array):
        """
        基于文本列表构建训练数据集
        """
        config=self.config
        model, vocab, label_dic=self.model, self.vocab, self.label_dic
        new_content_array=[]
        content_dict={}
        for i, content in enumerate (content_array):
            new_content_array.append(" ".join(list(content)))
            # content_dict[i]=content
        # print(content)
        # print(content_dict)
        input_data = build_input(content=new_content_array, max_length=self.config.max_length, vocab=self.vocab)
        # print(input_data)
        input_ids = torch.LongTensor([temp.input_id for temp in input_data])
        input_masks = torch.LongTensor([temp.input_mask for temp in input_data])

        input_dataset = TensorDataset(input_ids, input_masks)
        input_loader = DataLoader(input_dataset, shuffle=True, batch_size=self.config.batch_size)
        return input_loader

    def pre(self,content_array=[]):
        """
        执行预测
        输入多个句子即可
        """

        
        config=self.config
        model, vocab, label_dic=self.model, self.vocab, self.label_dic

        content_dict={}
        for i, content in enumerate (content_array):
            # new_content_array.append(" ".join(list(content)))
            content_dict[i]=content

        output=[]
        for i, batch in enumerate(self.build_input(content_array)):
            inputs, masks = batch
            # print('inputs',inputs)
            inputs, masks= Variable(inputs), Variable(masks)
            # print("masks",masks)
            if self.config.use_cuda:
                inputs, masks = inputs.cuda(), masks.cuda()
            feats = model(inputs)
            # print("feats",feats)
            path_score, best_path = model.crf(feats, masks.bool())
            # print("feats",path_score, best_path)
            for item in best_path.numpy():
                # print(item.tolist())
                words=[]
                for n,id in enumerate( item.tolist()):
                    word_id=inputs.numpy().tolist()[0][n]
                    l=list(label_dic)[id]
                    w=list(self.vocab)[word_id]
                    words.append((w,l))

                # print('words',words)
                wd={"type":None,"words":[]}
                wd_list=[]
                for w,l in words:
                    # print(wd)
                    if l.startswith("B-"): 
                        wd["type"]=l.split("B-")[1]
                        wd["words"].append(w)
                    elif l.startswith("M-"):
                        wd["type"]=l.split("M-")[1]
                        wd["words"].append(w)
                    elif l.startswith("E-"):
                        wd["type"]=l.split("E-")[1]
                        wd["words"].append(w)
                        wd_list.append(wd)
                        wd={"type":None,"words":[]}
                    elif l.startswith("S-"):
                        wd["type"]=l.split("S-")[1]
                        wd["words"].append(w)
                        wd_list.append(wd)
                        wd={"type":None,"words":[]}
                # print('wd_list',wd_list)
                # print(i)
                output.append((content_dict[i],wd_list))
        return output






def pre_one(**kwargs):
    # content="柯基犬性格活泼可爱，但是饲养柯基犬会有着六个坏处，你还敢饲养柯基犬吗？"
    # print(**kwargs)
    P=Pre()
    result=P.pre([kwargs['text']])
    print(result)
    




if __name__ == '__main__':
    fire.Fire()
    # test()










