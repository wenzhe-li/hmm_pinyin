import json

with open('cut_word.json', 'r', encoding='utf-8') as json_file:
    words = json.load(json_file)

words = words['cut_word']


def bag():
    print('loading')
    word_bag = {}
    for word in words:
        for w in word:
            if w in word_bag:
                word_bag[w] += 1
            else:
                word_bag[w] = 1
    with open('word_bag.json', 'w', encoding='utf-8') as json_file:
        json.dump(word_bag, json_file)


if __name__ == '__main__':
    bag()