# -*- coding: utf-8 -*-

# Imports
import os
import re
from collections import Counter
from string import punctuation


def save_censor_dict(censor_dict):
    with open('reverse_censor.txt', 'w', encoding = 'utf-8') as dict_file:
        for key in censor_dict.keys():
            dict_file.write(key+','+censor_dict[key]+'\n')
            
def get_censor_dict():
    dicty = {}
    dict_file = open('reverse_censor.txt', 'r', encoding = 'utf-8')
    lines = dict_file.readlines()
    dict_file.close()
    for line in lines:
        edit_line = line.rstrip('\n')
        dict_entry = edit_line.split(',')
        dicty[dict_entry[0]] = dict_entry[1]
    return dicty

def remove_punct(s):
    x = re.compile('[' + re.escape(punctuation.replace('*','')) + ']')
    output = x.sub('', s)
    return output

reverse_censor = get_censor_dict()
dat = []
for file in os.listdir('scripts'):
    file_title = file.replace('.txt', '')
    print(file_title)
    with open('scripts/' + file, 'r', encoding = 'utf-8') as read_file:
        text = read_file.read()
    text = text.replace('\n',' ').strip().lower()
    text = remove_punct(text)
    one_grams = re.split('\s+',text)
    len(one_grams)
    counter = Counter()
    counter.update(one_grams)
    
    with open('dicts/' + file, 'w', encoding = 'utf-8') as write_file:
        for word, count in counter.most_common():
            if not re.search('\w\*\w', word):
                trans_word = word
            elif word in reverse_censor.keys():
                trans_word = reverse_censor[word]
            else:
                trans_word = input(prompt = 'Translate ' + word + ': ')
                reverse_censor[word] = trans_word
            write_file.write(trans_word+','+'{s}'.format(s=counter[word])+'\n')
    
