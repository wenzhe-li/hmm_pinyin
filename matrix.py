import json
import numpy as np
import scipy.sparse as sp

from dataset_utils import *

with open('hz2id.json', 'r', encoding='utf-8') as json_file:
    hz2id = json.load(json_file)
hz2id = hz2id['hz2id']


def transition_p():
    with open('dataset.json', 'r', encoding='utf-8') as json_file:
        dataset = json.load(json_file)
    content = dataset['content']
    title = dataset['title']

    transition = np.ones([CHARACTERS, CHARACTERS], float)
    print('Loading content')
    for line in content:
        length = len(line)
        for i in range(length-1):
            if line[i] in hz2id and line[i+1] in hz2id:
                transition[hz2id[line[i]]][hz2id[line[i+1]]] += 1
    print('Loading title')
    for line in title:
        length = len(line)
        for i in range(length-1):
            if line[i] in hz2id and line[i+1] in hz2id:
                transition[hz2id[line[i]]][hz2id[line[i+1]]] += 1
    row_sum = np.sum(transition, axis=1)
    transition = np.log(transition / row_sum)
    '''for i in range(CHARACTERS):
        for j in range(CHARACTERS):
            if transition[i][j] != 0:
                transition[i][j] = np.log(transition[i][j] / row_sum[i])
            else:
                transition[i][j] = float('-inf')'''
    coo = sp.coo_matrix(transition)
    sp.save_npz('transition.npz', coo)
    return


def emission_p():
    with open('./dataset/table/py2hz.txt', 'r', encoding='gbk') as f:
        lines = f.readlines()
    py_dict = dict()
    emission = np.zeros([CHARACTERS, PYS], float)
    for i in range(PYS):
        py, characters = lines[i].split()[0], lines[i].split()[1:]
        py_dict[py] = i
        for c in characters:
            emission[hz2id[c]][i] += 1
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
    with open('cut_word.json', 'r', encoding='utf-8') as json_file:
        words = json.load(json_file)
    words = words['cut_word']
    initial = np.zeros([CHARACTERS,], float)
    cnt = 0
    for word in words:
        cnt += len(word)
        for w in word:
            if w[0] in hz2id:
                initial[hz2id[w[0]]] += 1
    for i in range(CHARACTERS):
        if initial[i] != 0:
            initial[i] = np.log(initial[i] / cnt)
        else:
            initial[i] = float('-inf')
    coo = sp.coo_matrix(initial)
    sp.save_npz('initial.npz', coo)
    return


if __name__ == '__main__':
    emission_p()