import os
import numpy as np
from tqdm import tqdm
import jieba
from time import time
import keras
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation,LSTM
from keras.layers import GlobalMaxPooling1D
from keras.layers import Dense, Input, Flatten
from keras.layers import Conv1D, MaxPooling1D, Embedding,Bidirectional
import datetime
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from sklearn.model_selection import train_test_split
import pickle
import jieba
from keras.layers import *
from keras.engine import Input
from keras.preprocessing.text import Tokenizer,  text_to_word_sequence
from keras.engine.topology import Layer
from keras import initializers as initializers, regularizers, constraints
from keras.callbacks import Callback, ModelCheckpoint
from keras.utils.np_utils import to_categorical
from keras.layers import Embedding, Input, Dense, LSTM, GRU, Bidirectional, TimeDistributed
from keras import backend as K
from keras import optimizers
from keras.models import Model




import pandas as pd
import time as time
##定义函数
def doc_pre(path,nb_classes):
    print('读取并准备文本数据...')
    dirname = path
    doc_all = []
    labels = []
    for dir_path, dir_name, files in tqdm(os.walk(dirname)):
        # 类别名称
        if dir_name:
            class_names = dir_name
        # 类别目录下的文本
        if not dir_name:
            for file in tqdm(files[:21000]):
                words = []
                txt_name = os.path.join(dir_path, file)
                try:
                    f = open(txt_name,'r+',encoding='GB18030').read()
                    print(f)  # , encoding='GB18030'
                    doc_all.append(f)
                    labels.append(class_names.index(os.path.split(dir_path)[1]))

                except UnicodeDecodeError as e:
                    continue

    # txts = np.array(txts)
    labels = keras.utils.np_utils.to_categorical(labels, nb_classes)
    return doc_all,labels


def cut_doc_2_sentences(doc, sentence_flags=None,
                        all_flags=None, strip_flags=None):
    '''
    :param doc: 要分句的text
    :param sentence_flags: 用来做分句标记的flags
    :param all_flags: 所有的标点，用于连续多个标点做成分句标示，todo
    :param strip_flags: 分句后删除句子前后的flag
    :return sentence_list: 最小成词长度
    '''
    if strip_flags is None:
        strip_flags = [' ']
    if sentence_flags is None:
        sentence_flags = [',', '.', '!', '?', ';', '~', '，', '。', '！', '？', '；', '～', '\n', ' ']
    last_flag = 0
    sentence_list = []
    doc_length = len(doc)
    for i in range(doc_length):
        if (i <= doc_length - 2 and doc[i] in sentence_flags and doc[
            i + 1] not in sentence_flags) or i == doc_length - 1:
            temp = doc[last_flag:i + 1]
            chars_no_flags = [char for char in temp if char not in sentence_flags]
            if len(chars_no_flags) < 3:
                # 句子内非标点句长小于阀值 3 的并入下一个分句
                continue
            # 分完句以后去掉前后无用的字符
            for flag in strip_flags:
                temp = temp.strip(flag)
            sentence_list.append(temp)
            last_flag = i + 1
    return sentence_list
# def pre_process_docs(docs):
# 将文章分词分句
def cut_docs(docs):
    start_time = time.time()
    print('start 分句...')
    docs_sentence_list = [cut_doc_2_sentences(doc) for doc in docs]
    print('end 分句,Total docs = {},Cost time = {}'.format(len(docs),time.time()-start_time))
    start_time = time.time()
    print('start 分词...')
    docs_cut = [[jieba.lcut(sentence) for sentence in sentence_list] for sentence_list in docs_sentence_list]
    print('end 分词, Cost time = {}'.format(time.time()-start_time))
    return docs_cut
# 根据训练集生成 vocabulary，返回 fit 后的 tokenizer
def build_vocabulary_tokenizer(docs_cut):
    vocabulary = []
    for doc_sentence_list in docs_cut:
        for sentence_list in doc_sentence_list:
            for word in sentence_list:
                vocabulary.append(word)
    tokenizer = keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts([vocabulary])
    return tokenizer
# 根据fit后的tokenizer，将分词分句后的doc中的词替换成index
def index_docs_func(tokenizer,docs_cut):
    index_docs = []
    for doc_sentence_list in docs_cut:
        index_docs.append(tokenizer.texts_to_sequences(doc_sentence_list))
    return index_docs
# doc_max_sentence_num, 文章最大句子数
# sentence_max_word_num，句子最大词数
# 将 doc_index padding 成相同的维度，补 0
def pad_docs(index_docs,doc_max_sentence_num,sentence_max_word_num,padding_value=0):
    data = []
    for doc in index_docs:
        doc_data = []
        for sentence in doc :
            # 句子 word 数补齐成 sentence_max_word_num
            if len(sentence)<sentence_max_word_num:
                sentence.extend([padding_value]*(sentence_max_word_num-len(sentence)))
            doc_data.append(sentence[:sentence_max_word_num])
        # 每篇文章句子数补够 doc_max_sentence_num
        if len(doc_data)<doc_max_sentence_num:
            doc_data.extend([[padding_value]*sentence_max_word_num]*(doc_max_sentence_num-len(doc_data)))
        data.append(doc_data[:doc_max_sentence_num])
    data = np.array(data)
    return data
# 预处理 训练集
def pre_process_train_docs(docs,doc_max_sentence_num,sentence_max_word_num):
    docs_cut = cut_docs(docs) # 分词分句
    start_time = time.time()
    print('start build_vocabulary_tokenizer...')
    tokenizer = build_vocabulary_tokenizer(docs_cut)
    print('end build_vocabulary_tokenizer, Cost time = {}'.format(time.time()-start_time))
    index_docs = index_docs_func(tokenizer,docs_cut)
    data = pad_docs(index_docs,doc_max_sentence_num,sentence_max_word_num)
    vocabulary_size = len(tokenizer.word_index.values()) + 1
    return data, vocabulary_size,tokenizer
# 预处理 验证集
def pre_process_val_docs(tokenizer,docs,doc_max_sentence_num,sentence_max_word_num):
    docs_cut = cut_docs(docs) # 分词分句
    index_docs = index_docs_func(tokenizer,docs_cut)
    data = pad_docs(index_docs,doc_max_sentence_num,sentence_max_word_num)
    return data

#数据处理
embedding_dim = 250 # 词向量的维度为100
rnn_unit_num = 150# rnn cell 的隐藏单元数量，也即：output_size/state_size
td_fc_unit_num = 200 # 双向 GRU 后 与 Attention 之间的 TimeDistributed fc
epochs = 5 # epoch
batch_size = 10 # 16
doc_max_sentence_num = 0# 文档中句子最多的数量
sentence_max_word_num =250# 句子中最大的词数量,sequence_length
class_num = 9 # 类别数量
drop_rate = 0.5 # drop_out 层的 drop 比例
try:
    data = pickle.load(open('d:/Sougou/data', 'rb'))
    labels = pickle.load(open('d:/Sougou/labels', 'rb'))
    tokenizer = pickle.load(open('d:/Sougou/tokenizer', 'rb'))
    vocabulary_size = pickle.load(open('d:/Sougou/vocabulary_size', 'rb'))

except:
    path = 'd:/Sougou/Reduced/'
    doc,labels = doc_pre(path,class_num)
    start_time = time.time()
    print('start pre_process_train_docs...')
    data, vocabulary_size ,tokenizer = pre_process_train_docs(doc,doc_max_sentence_num,sentence_max_word_num)

    pickle.dump(data, open('d:/Sougou/X_train', 'wb'))
    pickle.dump(labels, open('d:/Sougou/labels', 'wb'))
    pickle.dump(vocabulary_size, open('d:/Sougou/vocabulary_size', 'wb'))
    pickle.dump(tokenizer, open('d:/Sougou/tokenizer', 'wb'))

#X_train, X_test, Y_train, Y_test = train_test_split(data, labels, test_size=0.2, random_state=5)

print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')
print('building model')
