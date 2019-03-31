import json

with open('./dataset/table/hz_table.txt', 'r', encoding='gbk') as f:
    hz = f.read()

hz2id = dict()
cnt = 0

for c in hz:
    hz2id[c] = cnt
    cnt += 1

print(cnt)

result = dict()
result['hz2id'] = hz2id

with open('hz2id.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False)