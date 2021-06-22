#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

line_dict={}
movie_conversation=[]
def getLineid():
    for lines in open("movie_lines.txt","r",encoding="'iso-8859-1'"):
        rm=0
        line_ls=lines.split()
        for i,line in enumerate(line_ls):
            if(line=="+++$+++"):
                rm=i
        del line_ls[2:rm+1]
        line_dict[line_ls[0]]=" ".join(line_ls[2:])

def getConversation():
    for line in open("movie_conversations.txt","r",encoding="'iso-8859-1'"):
        #line_str=''.join(line.split()[6:]).replace('[','').replace(']','').replace(',',' ').replace("'",'')
        line_str=re.findall('(?<=\[).+?(?=\])',line)[0].replace(',',' ').replace("'",'')
        movie_conversation.append(line_str)

def makeIOfile():
    input_f=open("input_str.txt","w")
    output_f=open("output_str.txt","w")
    for lines in movie_conversation:
        lines_ls=lines.split()
        line_len=len(lines_ls)-1
        for i,line in enumerate(lines_ls):
            if(i%2==0 and i!=line_len):
                input_f.write(line_dict[line]+'\n')
            elif(i%2==1):
                output_f.write(line_dict[line]+'\n')
    input_f.close()
    output_f.close()



if __name__=='__main__':
    getLineid()
    getConversation()
    makeIOfile()
