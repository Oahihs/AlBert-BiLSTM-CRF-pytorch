# coding=utf-8
from utils import load_vocab, read_corpus, load_model, save_model,Tjson
from tqdm import tqdm
#         # return ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "[CLS]","[SEP]"]
#         return ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "X","[CLS]","[SEP]"]
import Terry_toolkit as tkit

def load_data():
    file="data/SAOKE_DATA.json"
    for  line in Tjson(file_path=file).load():
        print("##"*30)
        # print("line",line)
        print(line['natural'])
        # print(line['natural'])
        for it in line['logic']:
            print(it)
            # subject =line['natural'].find(it['subject'])
            # print(subject)
            print(find_srt(line['natural'],it['subject']))
            print(find_srt(line['natural'],it['predicate']))
            print(find_srt(line['natural'],it['object'][0]))
            print(it['subject'],it['predicate'],it['object'])

def find_srt(text,str):
    start =text.find(str)
    if start>=0:
        end=start+len(str)
        return start,end
    else:
        return None
        

    print(s)

load_data()