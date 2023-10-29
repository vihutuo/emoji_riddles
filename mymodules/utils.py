import random
import csv
def ShuffleString(s):
  L1=list(s)
  random.shuffle(L1)
  return "".join(L1)
  
def ReadCSV(filename):
    with open(filename, mode ='r')as file:
       csvFile = list(csv.reader(file))
    return csvFile 
           
def GetRandomWord(file_name):
    with open(file_name,"r") as f:
        L1=f.read().splitlines()
    print(len(L1))    
    return random.choice(L1)
def GetAllWords(file_name):
    with open(file_name,"r") as f:
        L1=f.read().splitlines()
    return L1  