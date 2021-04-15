# -*- coding: utf-8 -*-

import pickle as pk

dict_word={}
word_number=1
dict_word["<PAD>"]=0

def change_id(file_name,write_name):
    global word_number
    with open(file_name,"r") as f:
        with open(write_name,"w") as w:
            for str_line in f:
                id_str=[]
                for word in str_line.split():
                    if word in dict_word:
                        id_str.append(dict_word[word])
                    else:
                        word_number=word_number+1
                        dict_word[word]=word_number
                        id_str.append(dict_word[word])
                w.write(' '.join(map(str,id_str))+"\n")
                id_str.clear()

if __name__=="__main__":
    change_id("../data/input_str.txt","./data/input_id.txt")
    change_id("../data/output_str.txt","./data/output_id.txt")
    print(word_number)
    with open("../data/dict_word.pkl","wb") as p:
        pk.dump(dict_word,p)
