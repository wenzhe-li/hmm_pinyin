import jieba
import json
import re

jieba.initialize()

with open('dataset.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# filtrate the punctuation
filterate = re.compile(u'[^\u4E00-\u9FA5]')

content = data['content']
title = data['title']

word_bag = {}

print('content')
for line in content:
    print('loading')
    line = filterate.sub(r' ', line)
    # simplify the whitespace
    line = re.sub('\s\s+', ' ', line)
    seg_list = jieba.lcut(line, cut_all=False, HMM=True)
    while ' ' in seg_list:
        seg_list.remove(' ')
    for w in seg_list:
        if w in word_bag:
            word_bag[w] += 1
        else:
            word_bag[w] = 1

print('title')
for line in title:
    print('loading')
    line = filterate.sub(r' ', line)
    # simplify the whitespace
    line = re.sub('\s\s+', ' ', line)
    seg_list = jieba.lcut(line, cut_all=False, HMM=True)
    while ' ' in seg_list:
        seg_list.remove(' ')
    for w in seg_list:
        if w in word_bag:
            word_bag[w] += 1
        else:
            word_bag[w] = 1

with open('word_bag.json', 'w', encoding='utf-8') as json_file:
    json.dump(word_bag, json_file, ensure_ascii=False)