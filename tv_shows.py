# -*- coding: utf-8 -*-

# Imports
import requests
from bs4 import BeautifulSoup
import re
import os
import random

#path = '~OneDrive/Documents/UVM/Complex Networks/HW19/scripts/'
path = 'scripts/'
index_url = 'http://transcripts.foreverdreaming.org/viewforum.php?f=135/viewtopic.php?f=135'

def getLinks(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))

    return links

def getAllLinks(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    links = []
    for link in soup.findAll('a'):
        url = link.get('href')
        if (url[0] != '#'):
            links.append(url)
    return links

#print(getAllLinks(url))

def get_index_urls(index_url):
    initial_urls = getAllLinks(index_url)
    index_url_nums = []
    for url in initial_urls:
        search_result = re.search('&start=\d+$', url)
        if search_result != None:
            index_url_nums.append(int(search_result.group()[7:]))
    
    max_num = 0
    try:
        max_num = max(index_url_nums)
    except:
        pass
    num = 25
    index_urls = []
    while num <= max_num:
        index_urls.append(index_url + '&start=' + str(num))
        num += 25
    return initial_urls, index_urls
    
def get_all_tv_show_transcripts(index_url, path, txt_file_name):
    initial_urls, index_urls = get_index_urls(index_url)
    file = open(path + txt_file_name + '.txt', 'w', encoding='utf-8')
    title = get_tv_show_transcript(file, initial_urls, txt_file_name, True)
    for url in index_urls:
        initial_urls = getAllLinks(url)
        title = get_tv_show_transcript(file, initial_urls, title)
    file.close()
    print(title)
    title_alt = title.replace(':', '')
    title_alt = title_alt.replace('/', ' slash ')
    os.rename(path + txt_file_name + '.txt', path + title_alt + '.txt')
    

def get_tv_show_transcript(file, initial_urls, title, get_title = False):
    urls = []
    for url in initial_urls:
        search_result = re.search('f=\d+&t=\d+&', url)
        if search_result != None:
            urls.append('http://transcripts.foreverdreaming.org/viewtopic.php?'
                        + search_result.group()[:-1]
                        + '&view=print')
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if re.search('\d{2}x\d{2}', soup.title.text) != None:
            if get_title:
                title = soup.title.text.split(' - ')[-1]
            txt = soup.text
            txt = txt[txt.find('Post subject:'):]
            file.write(txt)
    return title


#get_all_tv_show_transcripts(index_url, path, 'AHS')
    
def get_all_index_urls():
    fnums = [1,595,892,596,71,894,503,775,2,895,896,593,335,893,897,3,898,597,4,325,899,900,901,1059,592,1060,940]
    all_index_nums = set()
    for fnum in fnums:
        index_url = 'http://transcripts.foreverdreaming.org/viewforum.php?f=' + str(fnum)
        initial_urls = getAllLinks(index_url)
        index_url_nums = []
        for url in initial_urls:
            search_result = re.search('f=\d+', url)
            if search_result != None:
                index_url_nums.append(int(search_result.group()[2:]))
        nums_set = set(index_url_nums)
        nums = nums_set.difference(set(fnums))
        all_index_nums = all_index_nums.union(nums)
    return list(all_index_nums)

'''all_index_urls = get_all_index_urls()
random.shuffle(all_index_urls)
all_index_urls = ['http://transcripts.foreverdreaming.org/viewforum.php?f=' + str(x) for x in all_index_urls]'''

# Now download text files for all of the TV shows
def write_txt_files(index_start, index_stop, urls):
    length = index_stop - index_start + 1
    for i in range(index_start, index_stop + 1):
        url = urls[i]
        get_all_tv_show_transcripts(url, path, 'placeholder')
        print('({s1}/{s2}) text files downloaded.'.format(s1=i-index_start+1,s2=length))

'''with open('all_index_urls.txt', 'w', encoding = 'utf-8') as file:
    for url in all_index_urls:
        file.write(url+'\n')'''

with open('all_index_urls.txt', 'r', encoding = 'utf-8') as file:
    all_index_urls = file.readlines()
all_index_urls = [x.replace('\n', '') for x in all_index_urls]


# comment whether done yet
write_txt_files(0,20,all_index_urls) #
write_txt_files(21,40,all_index_urls) #
write_txt_files(41,60,all_index_urls) #
write_txt_files(61,80,all_index_urls) #
write_txt_files(81,100,all_index_urls) #
write_txt_files(101,120,all_index_urls) # 
write_txt_files(121,140,all_index_urls) #
write_txt_files(141,160,all_index_urls) #
write_txt_files(161,180,all_index_urls) # 
write_txt_files(181,200,all_index_urls) #
write_txt_files(201,220,all_index_urls) #
write_txt_files(221,240,all_index_urls) #
write_txt_files(241,260,all_index_urls) #
write_txt_files(261,280,all_index_urls) #
write_txt_files(281,300,all_index_urls) #
write_txt_files(301,320,all_index_urls) #
write_txt_files(321,340,all_index_urls) #
write_txt_files(341,360,all_index_urls) #
write_txt_files(361,380,all_index_urls) #
write_txt_files(381,400,all_index_urls) #
write_txt_files(401,420,all_index_urls) #
write_txt_files(421,440,all_index_urls) #
write_txt_files(441,460,all_index_urls) #
write_txt_files(461,480,all_index_urls) #
write_txt_files(481,500,all_index_urls) #
