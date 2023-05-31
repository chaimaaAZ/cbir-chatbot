import random 
import json 
import torch 
from model import NeuralNet
from nmtk_utils import bag_of_word, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open("training.json","r") as f :
    intents =json.load(f)



data=torch.load("data.pth")
input_size=data["input_size"]
output_size=data["output_size"]
hidden_size=data["hidden_size"]
all_words=data["all_words"]
tags=data['tags']
model_state=data["model_state"]

model=NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name="kendall"

def get_response(msg) :
    sentence=tokenize(msg)
    X=bag_of_word(sentence,all_words)
    X=X.reshape(1,X.shape[0])
    X=torch.from_numpy(X).to(device)

    output=model(X)
    _,predicted=torch.max(output,dim=1)
    tag=tags[predicted.item()]

    probability=torch.softmax(output,dim=1)
    probability=probability[0][predicted.item()]

    if probability.item()>0.1 :
        for intent in intents["intents"] :
            if tag==intent["tag"] :
                return random.choice(intent['responses'])
    else :
        return "i do not understand..."


   
   