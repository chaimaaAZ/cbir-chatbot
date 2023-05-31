import json 
from nmtk_utils import tokenize , stem ,bag_of_word
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


with open(r"C:\Users\Chaimaa\Documents\data\python\image search engine 2\chatbot\training.json","r") as f:
    intents=json.load(f)

all_words=[]
tags=[]
xy=[]

for intent in intents['intents'] :
    tag=intent['tag']
    tags.append(tag)
    for pattern in intent['patterns'] :
       w= tokenize(pattern)
       all_words.extend(w)
       xy.append((w,tag))

ignore_words=['?','!','.',',']

#all_words =[stem(w) for w in all_words]
#set()--> remove duplicate elements 
#all_words=sorted(set(all_words))
#tag=sorted(set(tags))
#print(all_words)

X_train=[]
Y_train=[]

for (pattern_sentence,tag) in xy :
    bag=bag_of_word(pattern_sentence,all_words)
    X_train.append(bag)
    #to get index of the used tag
    label =tags.index(tag)

    Y_train.append(label) #crowwEntrepyLoss

X_train=np.array(X_train)
Y_train=np.array(Y_train)

class ChatDataset(Dataset) :
    def __init__(self) :
        self.n_samples=len(X_train)
        self.x_data=X_train
        self.y_data=Y_train
    
    #dataset[idx]
    def __getitem__(self, index) :
        return self.x_data[index],self.y_data[index]
    
    def __len__(self) :
        return self.n_samples
#hyper parameters
batch_size=8
dataset=ChatDataset()
train_loader=DataLoader(dataset=dataset,batch_size=batch_size,shuffle=True,num_workers=0)
