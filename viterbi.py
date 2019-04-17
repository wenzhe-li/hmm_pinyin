# -*- coding: gbk -*-

import json
import sys
import numpy as np
import scipy.sparse as sp
import pdb

from dataset_utils import *

print('Loading the data')
with open('hz2id.json', 'r', encoding='utf-8') as json_file:
    hz2id = json.load(json_file)
hz2id = hz2id['hz2id']

with open('py.json', 'r', encoding='utf-8') as json_file:
    py = json.load(json_file)
py = py['py']

with open('./dataset/table/py2hz.txt', 'r', encoding='gbk') as f:
    lines = f.readlines()

transition1 = sp.load_npz('transition1.npz').toarray()
transition2 = sp.load_npz('transition2.npz').toarray()
print(transition1.shape)
print(transition2.shape)
print(transition1)
print(transition2)
emission = sp.load_npz('emission.npz').toarray()
initial = sp.load_npz('initial.npz').toarray()
tail = sp.load_npz('tail.npz').toarray()
# print(transition[hz2id['机']][hz2id['系']])
# print(transition[hz2id['机']][hz2id['洗']])
print('Loaded successfully')

def viterbi(py_str):
    observe_seq = [py[s] for s in py_str.split()]
    T = {}
    head = observe_seq[0]
    states = [c for c in lines[head].split()[1:]]
    # print(states)
    for state in states:
        if state in hz2id:
            T[state] = ([state], initial[0][hz2id[state]])
    for output in observe_seq[1:]:
        # print(T)
        U = {}
        next_states = [c for c in lines[output].split()[1:]]
        # print(next_states)
        for next_state in next_states:
            # pdb.set_trace()
            if next_state in hz2id:
                argmax = None
                ml = float('-inf')
                # print(T)
                for state in states:
                    (path, p) = T[state]
                    tmp = emission[hz2id[next_state]][output] +\
                        transition1[hz2id[state]][hz2id[next_state]]
                    if len(path) > 1 and path[-2] in hz2id:
                        print(path, next_state)
                        tmp += transition2[hz2id[path[-2]]][hz2id[next_state]]
                    # if state == '机' and (next_state == '洗' or next_state == '系'):
                        # print('state', state, 'next_state', next_state, 'emission', emission[hz2id[next_state]][output], 'transition', transition[hz2id[state]][hz2id[next_state]])
                    p += tmp
                    if p >= ml:
                        argmax = path + [next_state]
                        ml = p
                if argmax is None:
                    print(path, tmp, p)
                U[next_state] = (argmax, ml)
                # print(U)
        
        T = U
        
        states = next_states
        
        # print(T)
        
    
    '''for state in states:
        (path, p) = T[state]
        p += tail[0][hz2id[state]]
        T[state] = (path, p)'''
    
    ml = float('-inf')
    result = []
    for k, (path, p) in T.items():
        if p > ml:
            result = path
            ml = p
    print('result', result)
    return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('please add paths of input file and output file')
        sys.exit()
    path_i = sys.argv[1]
    path_o = sys.argv[2]
    with open(path_i, 'r', encoding='utf-8') as f:
        input_str = f.readlines()
    output_str = []
    '''for s in input_str:
        output_str.append(''.join(viterbi(s)))'''
    for s in input_str:
        try:
            output_str.append(''.join(viterbi(s)))
        except:
            output_str.append(s)
    with open(path_o, 'w', encoding='utf-8') as f:
        for s in output_str:
            f.write(s + '\n')
    