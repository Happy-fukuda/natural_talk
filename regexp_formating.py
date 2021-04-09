# -*- coding: utf-8 -*-
import re

with open ("./make-meidai-dialogue/sequence.txt","r") as f:
    with open("sequence.txt","w") as w:
        for str in f:
            #print(str)
            str2=re.sub("\（.+?\）", "", str)
            str3=re.sub("F\d*","human",str2)
            w.write(str3)
