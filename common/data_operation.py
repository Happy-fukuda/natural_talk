# -*- coding: utf-8 -*-

import numpy
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pickle as pk


class DataOperation():
    def data_load(self,input_id="../data/input_id.txt",output_id="../data/output_id.txt",seed=1984):
        with open("../data/dict_word.pkl","rb") as f:
            self.dict_word,self.dict_num = pk.loads(f)
        int_input=[map(int,str_num.split()) for str_num in open(input_id,"r")]
        int_output=([map(int,str_num.split()) for str_num in open(output_id,"r")]
        input_max=0
        output_max=0
        for i in int_input:
            if input_max<len(i):
                input_max=len(i)
        for i in int_output:
            if output_max<len(i):
                output_max=len(i)
        np_input = keras.preprocessing.sequence.pad_sequences(int_input,
                                                        value=self.dict_word["<PAD>"],
                                                        padding='post',
                                                        maxlen=input_max)
        np_output = keras.preprocessing.sequence.pad_sequences(int_output,
                                                        value=self.dict_word["<PAD>"],
                                                        padding='post',
                                                        maxlen=output_max)
        split_num=len(np_input)-len(np_input)//10
        self.input_train , self.input_test = np_input[:split_num] , np_input[split_num:]
        self.output_train , self.output_test = np_output[:split_num] , np_output[split_num:]

        return (self.input_train,self.input_test) , (self.output_train , self.output_test)

    def word_dict(self):
        return self.dict_word,self.dict_num