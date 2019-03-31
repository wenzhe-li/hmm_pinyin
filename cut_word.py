import jieba
import json
import re

jieba.initialize()

with open('dataset.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# filtrate the punctuation
filterate = re.compile(u'[^\u4E00-\u9FA5]')

content = data['content']
cut_word = list()
for line in content:
    line = filterate.sub(r' ', line)
    # simplify the whitespace
    line = re.sub('\s\s+', ' ', line)
    seg_list = jieba.lcut(line, cut_all=False, HMM=True)
    while ' ' in seg_list:
        seg_list.remove(' ')
    cut_word.append(seg_list)

result = dict()
result['cut_word'] = cut_word

with open('cut_word.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False)