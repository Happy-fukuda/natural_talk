# -*- coding: utf-8 -*-
import re

def normalization():
    with open ("../make-meidai-dialogue/sequence.txt","r") as f:
        with open("../data/sequence.txt","w") as w:
            for str in f:
                #print(str)
                str2=re.sub("\（.+?\）", "", str)
                str3=re.sub("F\d*","human",str2)
                str4=re.sub(r"[,.!?:;' ]", "",str3)
                w.write(str4)
