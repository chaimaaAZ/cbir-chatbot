import json 

with open('index.json', 'r') as file:
          data = json.load(file)
          for dict in data :
            print(dict["image"])