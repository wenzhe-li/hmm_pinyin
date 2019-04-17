import json
import numpy as np

from dataset_utils import *

with open('transition2.json', 'r', encoding='utf-8') as json_file:
	transition2 = json.load(json_file)

mini = {}

for k1 in transition2.keys():
	mini[k1] = {}
	for k2 in transition2[k1].keys():
		mini[k1][k2] = {}
		for k3 in transition2[k1][k2].keys():
			s = 0
			if transition2[k1][k2][k3] > 3:
				s += transition2[k1][k2][k3]
				mini[k1][k2][k3] = transition2[k1][k2][k3] + 1
			s += CHARACTERS
			mini[k1][k2]['sum'] = s

for k1 in mini.keys():
	for k2 in mini[k1].keys():
		s = mini[k1][k2]['sum']
		for k3 in mini[k1][k2].keys():
			if k3 != 'sum':
				mini[k1][k2][k3] = np.log(mini[k1][k2][k3] / s)
		mini[k1][k2]['none'] = np.log(1 / s)		

with open('transition2_mini.json', 'w', encoding='utf-8') as json_file:
	json.dump(mini, json_file, ensure_ascii=False)

