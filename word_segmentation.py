# -*- coding: utf-8 -*-

import MeCab


def delethead(str_line):
    input_str=""
    output_str=""
    if "input:" in str_line:
        input_str=str_line.replace("input:","")
    elif "output:" in str_line:
        output_str=str_line.replace("output:","")

    return (input_str,output_str)




if __name__=="__main__":
    wakati = MeCab.Tagger("-Owakati")
    input_txt=open("./data/input_str.txt","w")
    output_txt=open("./data/output_str.txt","w")
    with open("sequence.txt","r") as f:
        for str in f:
            input_str,output_str=delethead(str)
            if input_str:
                input_txt.write(wakati.parse(input_str))
            else:
                output_txt.write(wakati.parse(output_str))
