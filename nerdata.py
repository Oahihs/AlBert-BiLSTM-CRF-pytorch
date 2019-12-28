# coding=utf-8
from utils import load_vocab, read_corpus, load_model, save_model,Tjson
from tqdm import tqdm
#         # return ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "[CLS]","[SEP]"]
#         return ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "X","[CLS]","[SEP]"]
 

def _read_data( input_file):
    """Reads a BIO data."""
    with open(input_file) as f:
        lines = []
        words = []
        labels = []
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
                   lines.append([l, w])
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

    with open("data/tag.txt","w") as f:
        f.write("\n".join(tags.keys()))



input_files=["/mnt/data/dev/tdata/ner/dev.txt","/mnt/data/dev/tdata/ner/train.txt",'/mnt/data/dev/tdata/ner/test.txt','/mnt/data/dev/tdata/ner/example.train','/mnt/data/dev/tdata/ner/example.dev','/mnt/data/dev/tdata/ner/example.test','/mnt/data/dev/tdata/ner/dh_msra.txt','/mnt/data/dev/tdata/ner/weiboNER.2.txt','/mnt/data/dev/tdata/ner/weiboNER.1.txt','/mnt/data/dev/tdata/ner/weiboNER.3.txt']
run(input_files)