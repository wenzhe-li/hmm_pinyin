import json
import numpy as np
import scipy.sparse as sp

from dataset_utils import *

with open('hz2id.json', 'r', encoding='utf-8') as json_file:
    hz2id = json.load(json_file)
hz2id = hz2id['hz2id']

with open('py.json', 'r', encoding='utf-8') as json_file:
    py = json.load(json_file)
py = py['py']

with open('./dataset/table/py2hz.txt', 'r', encoding='gbk') as f:
    lines = f.readlines()

transition = sp.load_npz('transition.npz').toarray()
emission = sp.load_npz('emission.npz').toarray()
initial = sp.load_npz('initial.npz').toarray()

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
        
        for next_state in next_states:
            if next_state in hz2id:
                argmax = None
                ml = float('-inf')
                for state in states:
                    (path, p) = T[state]
                    tmp = emission[hz2id[next_state]][output] +\
                        transition[hz2id[state]][hz2id[next_state]]
                    # print(emission[hz2id[next_state]][output], transition[hz2id[state]][hz2id[next_state]])
                    p += tmp
                    if p > ml:
                        argmax = path + [next_state]
                        ml = p
                U[next_state] = (argmax, ml)
        T = U
        states = next_states
    # print(T)
    
    
    ml = float('-inf')
    result = []
    for k, (path, p) in T.items():
        if p > ml:
            result = path
            ml = p
    return result


if __name__ == '__main__':
    s = 'guo nian hui jia chi jiao zi'
    print(''.join(viterbi(s)))