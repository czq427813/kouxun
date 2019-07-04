#!/usr/bin/env python
# coding: utf-8


import os
import numpy as np
import requests
from bs4 import BeautifulSoup
import json


#词汇表导入
def wordList(route):
    wordList = {}
    for file in os.listdir(route):
        with open(route+file) as f:
            next(f) 
            for line in f: 
            
                temp = line.split("|" or " ")
                wordList[temp[0]] = 1  
    return wordList

"""
需要对词汇表进行小的修改，比如去掉"="这样
"""


def wordScreen(word, wordList):
    num = 0
    find = 0
    while find != 1 and num < len(wordList):
        #if wordList[num].has_key(word):
        if word in wordList[num]:
            find = 1
            return num
        else:
            num += 1
    return -1


def wordTranslate(word):
    url = "http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.top"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    links_trans = soup.find('div', class_="trans-container").text
    return links_trans
    


#同义词替换
def synoList(word, wordList):
    synoList = []
    url = "https://www.thesaurus.com/browse/"+word
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    links_syno = soup.find('ul', class_="css-1lc0dpe et6tpn80")
    for s in links_syno:
        if wordScreen(s.get_text(),wordList) != -1:
            synoList.append(s.get_text())
    if len(synoList) > 0:
        return ",".join(synoList)
    else:
        return "No suitable synonyms could be replaced"


def main(text):
    word = text  # 查询的单词
    level = ["小学","初一","初二","初三","中考"] #词汇表等级
    wordList = [
        {"word":1,"large":1,"X-man":1},
        {"school":1, "place":1,"seat":1},
        {"Florida":1},
        {"vocabulary":1,"test":1},
        {"camp":1, "bridge":1, "room":1}
    ]
    finalLevel = level[wordScreen(word, wordList)]
    #单词注释
    trans = wordTranslate(word).replace(" ","")
    new_trans = trans.replace("\n","")
    #同义词替换
    syno = synoList(word, wordList)
    final = {
        "level": {"level": finalLevel},
        "translate": {"translate": new_trans},
        "synonyms": {word: syno}
    }
    return json.dumps(final, ensure_ascii=False)


if __name__ == "__main__":
    #print(main("marvelyoshi"))
    print(main("place"))



