#!/usr/bin/env python
# coding: utf-8

# # Gal data Encoding functions by korBERT encoder

# In[ ]:


get_ipython().system('pip install keras-bert')
get_ipython().system('pip install keras-radam')


# In[ ]:


import glob
import pandas as pd
import numpy as np 

import os
from tqdm import tqdm

import codecs


# In[ ]:


from keras_bert import Tokenizer


# In[ ]:


# input을 txt로 받았을 때 데이터프레임을 만드는 함수
def make_table(txt_path):
    files = glob.glob(txt_path)  
    
    df =  pd.DataFrame(index=range(0,len(files)), columns=['idx', 'class','conversation'])
    i = 0
    for file in files:
        f = open(file, 'r', encoding="UTF-8")
        line = f.readlines()
        df['idx'][i] = i
        # df['class'][i] = #레이블달기 전이니까 빈칸
        df['conversation'][i] = line
        
        i += 1
    
    return df


# In[ ]:


#korBERT 사전으로 tokenize
pretrained_path ="./bert" #상대경로 잡기
vocab_path = os.path.join(pretrained_path, 'vocab.txt')

SEQ_LEN = 256
DATA_COLUMN = "conversation"
LABEL_COLUMN = "class"


# In[ ]:


#Token 딕셔너리 만들기
token_dict = {}
with codecs.open(vocab_path, 'r', 'utf8') as reader:
    for line in reader:
        token = line.strip()
        if "_" in token:
            token = token.replace("_","")
            token = "##" + token
        token_dict[token] = len(token_dict)
        #key(문자) = value(index)


# In[ ]:


# tokenizer 클래스 만들기
class inherit_Tokenizer(Tokenizer):
    def _tokenize(self, text):
        if not self._cased:
            text = text
            
            text = text.lower()
        spaced = ''
        for ch in text:
            if self._is_punctuation(ch) or self._is_cjk_character(ch):
                spaced += ' ' + ch + ' '
            elif self._is_space(ch):
                spaced += ' '
            elif ord(ch) == 0 or ord(ch) == 0xfffd or self._is_control(ch):
                continue
            else:
                spaced += ch
        tokens = []
        for word in spaced.strip().split():
            tokens += self._word_piece_tokenize(word)
        return tokens


# In[ ]:


tokenizer = inherit_Tokenizer(token_dict)


# In[ ]:


def convert_data(data_df): #korBERT의 토큰 딕셔너리로 데이터를 인코딩하는 함수
    global tokenizer
    indices, targets = [], []
    for i in tqdm(range(len(data_df))):
        ids, segments = tokenizer.encode(data_df[DATA_COLUMN][i], max_len=SEQ_LEN) # conversation
        indices.append(ids)
        targets.append(data_df[LABEL_COLUMN][i]) # class
    items = list(zip(indices, targets))
    
    indices, targets = zip(*items)
    indices = np.array(indices)
    return [indices, np.zeros_like(indices)], np.array(targets)


# In[ ]:


def load_data(pandas_dataframe): # 데이터 인코딩을 실행하는 함수
    data_df = pandas_dataframe
    
    
    data_df[DATA_COLUMN] = data_df[DATA_COLUMN].astype(str) # conversation


    data_x, data_y = convert_data(data_df)

    return data_x, data_y

