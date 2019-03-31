import json

strs = ['02', '04', '05', '06', '07', '08', '09', '10', '11']

news_content = list()
news_title = list()

for s in strs:
    print('Loading %s' % ('./dataset/sina_news_gbk/2016-' + s + '.txt'))
    with open('./dataset/sina_news_gbk/2016-' + s + '.txt', 'r', encoding='gbk') as f:
        lines = f.readlines()
    for line in lines:
        content = json.loads(line)
        news_content.append(content['html'])
        news_title.append(content['title'])

dataset = dict()
dataset['content'] = news_content
dataset['title'] = news_title

with open('dataset.json', 'w', encoding='utf-8') as json_file:
    json.dump(dataset, json_file, ensure_ascii=False)