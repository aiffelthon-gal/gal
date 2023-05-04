import pandas as pd
import numpy as np
import os

import tensorflow as tf
import keras as keras
from keras.models import load_model

import encoding_korbert as enc
import cleaning_and_normalizing as cleandnor

from keras_radam import RAdam
from keras_radam.training import RAdamOptimizer

from keras_bert import load_trained_model_from_checkpoint, load_vocabulary
from keras_bert import Tokenizer
from keras_bert import AdamWarmup, calc_train_steps


def encoding_txt_for_model(input_path):

    input_df = enc.make_table(input_path)
    input_df['conversation']= ''.join(input_df['conversation'][0])
    input_x, input_y = enc.load_data(input_df)
    
    return input_x


def string_to_input(str):
    df =  pd.DataFrame(index=[0], columns=['idx', 'class','conversation'])
    df['idx'] =0
    df['conversation'] = str
    
    input_x, input_y = enc.load_data(df)

    return input_x


#토큰 임베딩 불러오기
pretrained_path ="./bert" #상대경로 잡기
SEQ_LEN = enc.SEQ_LEN
config_path = os.path.join(pretrained_path, 'bert_config.json')
checkpoint_path = os.path.join(pretrained_path, 'bert_model.ckpt')

def build_model_1():
    model = load_trained_model_from_checkpoint(config_path,
                                                checkpoint_path,
                                                training=True,
                                                trainable=True,
                                                seq_len=SEQ_LEN)
    
    inputs = model.inputs[:2]
    dense = model.layers[-3].output
    
    outputs = keras.layers.Dense(1, activation='sigmoid', 
                               kernel_initializer=keras.initializers.TruncatedNormal(stddev=0.02, seed=1004),
                              name = 'real_output')(dense)

    bert_model = keras.models.Model(inputs, outputs)

    return bert_model

model_1 = build_model_1()


def build_model_2():
    model = load_trained_model_from_checkpoint(config_path,
                                                checkpoint_path,
                                                training=True,
                                                trainable=True,
                                                seq_len=SEQ_LEN)
    
    inputs = model.inputs[:2]
    dense = model.layers[-3].output
    
    outputs = keras.layers.Dense(4, activation='softmax', 
                               kernel_initializer=keras.initializers.TruncatedNormal(stddev=0.02, seed=1004),
                              name = 'real_output')(dense)

    bert_model = keras.models.Model(inputs, outputs)
    return bert_model

model_2 = build_model_2()

def build_model_3():
    model = load_trained_model_from_checkpoint(config_path,
                                                checkpoint_path,
                                                training=True,
                                                trainable=True,
                                                seq_len=SEQ_LEN)
    
    inputs = model.inputs[:2]
    dense = model.layers[-3].output
    
    outputs = keras.layers.Dense(5, activation='softmax', 
                               kernel_initializer=keras.initializers.TruncatedNormal(stddev=0.02, seed=1004),
                              name = 'real_output')(dense)

    bert_model = keras.models.Model(inputs, outputs)

    return bert_model

model_3 = build_model_3()


model_1.load_weights('./saved/model_1_weights_0427.h5')
model_2.load_weights('./saved/model_2_weights_0427.h5')
model_3.load_weights('./saved/model_3_weights_0427.h5')


def model_ens_1_and_2(input_x, threshold_min = 7.321e-06, threshold_max = 0.999):
    probs = model_1.predict(input_x)
    probs_2 = model_2.predict(input_x)
    class_dict = {0: '명시적인 언어폭력', 1: '일상적인 대화문', 2: '암묵적인 갈취 대화', 3: '암묵적인 기타 괴롭힘 대화', 4: '암묵적인 직장 내 괴롭힘 대화', 5: '암묵적인 협박 대화'}
    
    class_list = []
    for i in range(probs.shape[0]):
        p1 = probs[i]
        print(p1)
        if threshold_min < p1 < threshold_max:
            p2 = probs_2[i]
            print(p2)
            label = np.argmax(p2) +2
            class_list.append(class_dict[label])
            

        elif threshold_max <= p1 :
            label = 1
            class_list.append(class_dict[label])
        else :
            label = 0
            class_list.append(class_dict[label])
            
    preds = np.array(class_list)
   
    return class_dict[label]+'입니다.'


def model_ens_1_and_3(input_x, threshold = 7.321e-06):
    probs = model_1.predict(input_x)
    probs_3 = model_3.predict(input_x)
    class_dict = {0: '명시적인 언어폭력', 1: '암묵적인 갈취 대화', 2: '암묵적인 기타 괴롭힘 대화', 3: '일상적인 대화문', 4: '암묵적인 직장 내 괴롭힘 대화',5: '암묵적인 협박 대화'}
    
    class_list = []
    for i in range(probs.shape[0]):
        p1 = probs[i]
        print(p1)
        if p1 < threshold:
            label = 0
            class_list.append(class_dict[label])

        else :
            p3 = probs_3[i]
            print(p3)
            label = np.argmax(p3) +1
            class_list.append(class_dict[label])
            
  
    preds = np.array(class_list)
    
    return class_dict[label]+'입니다.'


def web_detect_1_2(str): #본모델
    
    x = string_to_input(str)
    return model_ens_1_and_2(x)
    

def web_detect_1_3(str): #서브모델
    
    x = string_to_input(str)
    return model_ens_1_and_3(x)

