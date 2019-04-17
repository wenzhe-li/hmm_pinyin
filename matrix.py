# -*- coding: gbk -*-

import json
import numpy as np
import scipy.sparse as sp

from dataset_utils import *
from pypinyin import lazy_pinyin

with open('hz2id.json', 'r', encoding='utf-8') as json_file:
    hz2id = json.load(json_file)
hz2id = hz2id['hz2id']

with open('word_bag.json', 'r', encoding='utf-8') as json_file:
        word_bag = json.load(json_file)

def prior_p():
    prior = np.ones([1, CHARACTERS], float)
    for (k, v) in word_bag.items():
        for i in range(len(k)):
            if k[i] in hz2id:
                prior[0][hz2id[k[i]]] += v
    row_sum = np.sum(prior, axis=1, keepdims=True)
    prior = np.log(prior / row_sum)
    coo = sp.coo_matrix(prior)
    sp.save_npz('prior.npz', coo)
    print(prior)

def transition_p():
    with open('dataset.json', 'r', encoding='utf-8') as json_file:
        dataset = json.load(json_file)
    content = dataset['content']
    title = dataset['title']

    transition1 = np.ones([CHARACTERS, CHARACTERS], float)
    transition2 = np.ones([CHARACTERS, CHARACTERS], float)
    print('Loading content')
    for line in content:
        length = len(line)
        for i in range(length-1):
            if line[i] in hz2id and line[i+1] in hz2id:
                transition1[hz2id[line[i]]][hz2id[line[i+1]]] += 1
            if i+2 < length:
                if line[i] in hz2id and line[i+2] in hz2id:
                    transition2[hz2id[line[i]]][hz2id[line[i+2]]] += 1
    print('Loading title')
    for line in title:
        length = len(line)
        for i in range(length-1):
            if line[i] in hz2id and line[i+1] in hz2id:
                transition1[hz2id[line[i]]][hz2id[line[i+1]]] += 1
            if i+2 < length:
                if line[i] in hz2id and line[i+2] in hz2id:
                    transition2[hz2id[line[i]]][hz2id[line[i+2]]] += 1
    row_sum1 = np.sum(transition1, axis=1)
    row_sum1 = row_sum1.reshape([CHARACTERS, 1])
    transition1 = np.log(transition1 / row_sum1)
    coo1 = sp.coo_matrix(transition1)
    sp.save_npz('transition1.npz', coo1)
    row_sum2 = np.sum(transition2, axis=1)
    row_sum2 = row_sum2.reshape([CHARACTERS, 1])
    transition2 = np.log(transition2 / row_sum2)
    coo2 = sp.coo_matrix(transition2)
    sp.save_npz('transition2.npz', coo2)
    return


def emission_p():
    with open('./dataset/table/py2hz.txt', 'r', encoding='gbk') as f:
        lines = f.readlines()
    py_dict = dict()
    emission = np.zeros([CHARACTERS, PYS], float)
    for i in range(PYS):
        py = lines[i].split()[0]
        py_dict[py] = i
    for (k, v) in word_bag.items():
        pinyin = lazy_pinyin(k)
        for i in range(len(k)):
            if pinyin[i] == 'n':
                pinyin[i] = 'en'
            if pinyin[i] == 'lve':
                pinyin[i] = 'lue'
            if pinyin[i] == 'nve':
                pinyin[i] = 'nue'
            if k[i] in hz2id and pinyin[i] in py_dict:
                emission[hz2id[k[i]]][py_dict[pinyin[i]]] += v
            elif not pinyin[i] in py_dict:
                print(pinyin[i])
    row_sum = np.sum(emission, axis=1)
    for i in range(CHARACTERS):
        for j in range(PYS):
            if emission[i][j] != 0:
                emission[i][j] = np.log(emission[i][j] / row_sum[i])
            else:
                emission[i][j] = float('-inf')    
    coo = sp.coo_matrix(emission)
    sp.save_npz('emission.npz', coo)
    py_table = dict()
    py_table['py'] = py_dict
    with open('py.json', 'w', encoding='utf-8') as json_file:
        json.dump(py_table, json_file)
    return


def initial_p():
    initial = np.ones([CHARACTERS,], float)
    for (k, v) in word_bag.items():
        if k[0] in hz2id:
            initial[hz2id[k[0]]] += v
    row_sum = np.sum(initial)
    initial = np.log(initial / row_sum)
    # print(initial)
    coo = sp.coo_matrix(initial)
    sp.save_npz('initial.npz', coo)
    return

def tail_p():
    tail = np.ones([CHARACTERS,], float) * 0.001
    for (k, v) in word_bag.items():
        if k[-1] in hz2id:
            tail[hz2id[k[-1]]] += v
    row_sum = np.sum(tail)
    tail = np.log(tail / row_sum)
    # print(tail)
    coo = sp.coo_matrix(tail)
    sp.save_npz('tail.npz', coo)
    return


if __name__ == '__main__':
    print('processing prior matrix')
    prior_p()
    print('processing transition matrix')
    #transition_p()
    print('processing emission matrix')
    #emission_p()
    print('processing initial matrix')
    #initial_p()
    print('processing tail matrix')
    #tail_p()