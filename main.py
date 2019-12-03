# coding=utf-8
import torch
import torch.nn as nn
from torch.autograd import Variable
from config import Config
from model import BERT_LSTM_CRF
import torch.optim as optim
from utils import load_vocab, read_corpus, load_model, save_model,build_input,Tjson
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
import fire

def test():
    """
    执行预测
    """
    config = Config()
    # config.update(**kwargs)
    print('当前设置为:\n', config)
    if config.use_cuda:
        torch.cuda.set_device(config.gpu)
    print('loading corpus')
    vocab = load_vocab(config.vocab)
    label_dic = load_vocab(config.label_file)
    tagset_size = len(label_dic)
    # content=["柯 基 犬 是 个 小 狗 子"]
    content=list("威尔士柯基犬（welsh corgi pembroke）是一种小型犬，它们的胆子很大，也相当机警，能高度警惕地守护家园，是最受欢迎的小型护卫犬之一。")
    content=" ".join(content)

    dev_json_save=Tjson(file_path="data/dev.json")
    data=[]
    for item in dev_json_save.load():
        print("#########"*5)
        content=" ".join(item['text'])
        print(content)
        print(item['label'])
        input_data = build_input(content=[content], max_length=config.max_length, vocab=vocab)


        input_ids = torch.LongTensor([temp.input_id for temp in input_data])
        input_masks = torch.LongTensor([temp.input_mask for temp in input_data])

        input_dataset = TensorDataset(input_ids, input_masks)
        input_loader = DataLoader(input_dataset, shuffle=True, batch_size=config.batch_size)

        model = BERT_LSTM_CRF(config.bert_path, tagset_size, config.bert_embedding, config.rnn_hidden, config.rnn_layer, dropout_ratio=config.dropout_ratio, dropout1=config.dropout1, use_cuda=config.use_cuda)
        if config.load_model:
            assert config.load_path is not None
            # 
            model = load_model(model, name=config.load_path)
        # model = load_model(model, name='result/pytorch_model.bin')
        if config.use_cuda:
            model.cuda()
        # model.train()
        for i, batch in enumerate(input_loader):
            inputs, masks = batch
            # print('inputs',inputs)
            inputs, masks= Variable(inputs), Variable(masks)
            # print("masks",masks)
            if config.use_cuda:
                inputs, masks = inputs.cuda(), masks.cuda()
            feats = model(inputs)
            # print("feats",feats)
            path_score, best_path = model.crf(feats, masks.bool())
            print("feats",path_score, best_path)
            for item in best_path.numpy():
                # print(item.tolist())
                words=[]
                for i,id in enumerate( item.tolist()):
                    word_id=inputs.numpy().tolist()[0][i]
                    words.append((list(vocab)[word_id],list(label_dic)[id]))
                print('words',words)


def train(**kwargs):
    config = Config()
    config.update(**kwargs)
    print('当前设置为:\n', config)
    # if config.use_cuda:
    #     torch.cuda.set_device(config.gpu)
    print('loading corpus')
    vocab = load_vocab(config.vocab)
    label_dic = load_vocab(config.label_file)
    tagset_size = len(label_dic)
    train_data = read_corpus(config.train_file, max_length=config.max_length, label_dic=label_dic, vocab=vocab)
    dev_data = read_corpus(config.dev_file, max_length=config.max_length, label_dic=label_dic, vocab=vocab)

    train_ids = torch.LongTensor([temp.input_id for temp in train_data])
    train_masks = torch.LongTensor([temp.input_mask for temp in train_data])
    train_tags = torch.LongTensor([temp.label_id for temp in train_data])

    train_dataset = TensorDataset(train_ids, train_masks, train_tags)
    train_loader = DataLoader(train_dataset, shuffle=True, batch_size=config.batch_size)

    dev_ids = torch.LongTensor([temp.input_id for temp in dev_data])
    dev_masks = torch.LongTensor([temp.input_mask for temp in dev_data])
    dev_tags = torch.LongTensor([temp.label_id for temp in dev_data])

    dev_dataset = TensorDataset(dev_ids, dev_masks, dev_tags)
    dev_loader = DataLoader(dev_dataset, shuffle=True, batch_size=config.batch_size)
    model = BERT_LSTM_CRF(config.bert_path, tagset_size, config.bert_embedding, config.rnn_hidden, config.rnn_layer, dropout_ratio=config.dropout_ratio, dropout1=config.dropout1, use_cuda=config.use_cuda)
    if config.load_model:
        assert config.load_path is not None
        model = load_model(model, name=config.load_path)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    # if config.use_cuda:
    #     model.cuda()
    model.train()
    optimizer = getattr(optim, config.optim)
    optimizer = optimizer(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)
    eval_loss = 10000
    for epoch in range(config.base_epoch):
        step = 0
        for i, batch in enumerate(train_loader):
            step += 1
            model.zero_grad()
            inputs, masks, tags = batch
            # print('inputs',inputs)
            inputs, masks, tags = Variable(inputs), Variable(masks), Variable(tags)
            # if config.use_cuda:
            #     inputs, masks, tags = inputs.cuda(), masks.cuda(), tags.cuda()
            inputs, masks, tags = inputs.to(device), masks.to(device), tags.to(device)
            feats = model(inputs, masks)
            # print("feats",feats)
            loss = model.loss(feats, masks,tags)
            loss.backward()
            optimizer.step()
            if step % 50 == 0:
                print('step: {} |  epoch: {}|  loss: {}'.format(step, epoch, loss.item()))
        loss_temp = dev(model, dev_loader, epoch, config)
        if loss_temp < eval_loss:
            save_model(model,epoch)


def dev(model, dev_loader, epoch, config):
    model.eval()
    eval_loss = 0
    true = []
    pred = []
    length = 0
    for i, batch in enumerate(dev_loader):
        inputs, masks, tags = batch
        length += inputs.size(0)
        inputs, masks, tags = Variable(inputs), Variable(masks), Variable(tags)
        # if config.use_cuda:
        #     inputs, masks, tags = inputs.cuda(), masks.cuda(), tags.cuda()
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        inputs, masks, tags = inputs.to(device), masks.to(device), tags.to(device)

        feats = model(inputs, masks)
        # path_score, best_path = model.crf(feats, masks.byte())
        path_score, best_path = model.crf(feats, masks.bool())
        loss = model.loss(feats, masks, tags)
        eval_loss += loss.item()
        pred.extend([t for t in best_path])
        true.extend([t for t in tags])
    print('eval  epoch: {}|  loss: {}'.format(epoch, eval_loss/length))
    model.train()
    return eval_loss


if __name__ == '__main__':
    fire.Fire()
    # test()










