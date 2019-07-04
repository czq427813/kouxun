#!/usr/bin/env python
# coding: utf-8

# In[7]:


from nltk.stem import WordNetLemmatizer
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, WordPunctTokenizer
from string import punctuation
import re
import json


# 设置stopwords 主要是各种标点符号
stopwords = set(stopwords.words('english') + list(punctuation) + [').'])

replace_patterns = [
    (r"can\'t", "cannot"),
    (r"won't", "will not"),
    (r"i'm", "i am"),
    (r"isn't", "is not"),
    (r"(\w+)'ll", "\g<1> will"),
    (r"(\w+)n't", "\g<1> not"),
    (r"(\w+)'ve", "\g<1> have"),
    (r"(\w+)'s", "\g<1> is"),
    (r"(\w+)'re", "\g<1> are"),
    (r"(\w+)'d", "\g<1> would"),
]


# 缩略词展开
class RegexpReplacer(object):

    def __init__(self, replace_patterns=replace_patterns):
        self.parrents = [(re.compile(regex), repl) for regex, repl in replace_patterns]

    def replace(self, text):
        for parrent, repl in self.parrents:
            text, count = re.subn(pattern=parrent, repl=repl, string=text)
        return text


"""
replacer = RegexpReplacer()
text = "The hard part isn't making the decision. It's living with it."
print(replacer.replace(text))
"""



"""
分段成句和分句成词
"""


def splitSentence(paragraph):
    sent = sent_tokenize(paragraph)
    return sent


# 测试
# if __name__ == '__main__':
#    print (splitSentence("My name is Tom. I am a boy. I like socer!"))

def wortokenizer(sentence):
    word = []
    words = WordPunctTokenizer().tokenize(sentence)
    word = word + words
    return word


# 测试
# if __name__ == '__main__':
#    print (wortokenizer ("My name is Tom."))



# 标准化单词
def standardization(word_sent):
    # 转换换成小写字母
    text = []
    for s in word_sent:
        text.append(s.lower())

    # 处理停用词和短词
    new_text = [word for word in text if word not in stopwords and 3 < len(word)]

    return new_text



# 词形还原
def lemmatizer(word):
    wnl = WordNetLemmatizer()
    text = []
    # 对单词类型标注
    text_tag = np.array(nltk.pos_tag(word))
    # print text_tag
    for s in text_tag:
        if s[1].startswith('N'):
            if s[1] == 'NNS' or s[1] == 'NN':
                text.append(wnl.lemmatize(s[0], 'n'))
        elif s[1].startswith('V'):
            text.append(wnl.lemmatize(s[0], 'v'))
        elif s[1].startswith('J'):
            text.append(wnl.lemmatize(s[0], 'a'))
        elif s[1].startswith('R'):
            text.append(wnl.lemmatize(s[0], 'r'))
        elif s[1] != 'CD':
            text.append(s[0])

    return text


"""
有些名词和副词无法还原，比如 best, better, Germans, Vikings这种

"""



def textProcessor(text):
    # 缩略词展开
    replacer = RegexpReplacer()
    para = replacer.replace(text)

    # 断句
    sent = para.split("###")

    # 分词
    word = []
    if len(sent) > 1:
        for i in sent:
            temp = wortokenizer(i)
            word = word + temp

    else:
        temp = wortokenizer(sent)
        word.append(temp)

    # 初步处理
    newList = standardization(word)

    # 词形还原
    finalList = lemmatizer(newList)
    return finalList


# In[31]:


"""
词汇表导入
"""
wordList = []
f = open("D:/Documents/Downloads/my_blog/filter/Unit1.txt")
next(f)
for line in f:
    temp = line.split("|")
    wordList.append(temp[0].lower())


def Word(text):
    # 统计超纲词
    superclassWord = {}

    articalword = textProcessor(text)
    for word in articalword:
        if word not in wordList:
            if not word in superclassWord:
                superclassWord[word] = 1
            else:
                superclassWord[word] = superclassWord[word] + 1
    # print superclassWord

    # 统计超纲词总数
    numSuperclassWord = 0
    for key, value in superclassWord.items():
        numSuperclassWord = numSuperclassWord + value

    final = {
        "text": text,
        "num": numSuperclassWord,
        'superclassWord': superclassWord

    }

    return final


if __name__ == "__main__":
    text = "SHANGHAI, June 22 — Women accounted for around 51###8 percent of moviegoers in China last year, showing their growing influence on the country's box office, a report on the country's film industry showed###More than half of viewers of the top 10 movies in terms of the box office in China in 2018 were women### The proportion of female moviegoers of domestic fantasy  and  each surpassed 60 percent, according to Liu Jia, one of the writers of the report###The stereotype about Chinese women who do not like action or sci-fi films has been broken### Last year, foreign and domestic blockbusters such as  and  have all attracted more female moviegoers than their male counterparts, it said###The report noted that Chinese female viewers' preference was not confined to romantic movies### They also played a leading role in the contribution to the box office for comedies, action, sci-fi and adventure films###The report was released by organizations including China Film Association at the ongoing 22nd Shanghai International Film Festival###"
    #text = "SHANGHAI, June 22 — Women accounted for around 51.8 percent of moviegoers in China last year, showing their growing influence on the country's box office, a report on the country's film industry showed.More than half of viewers of the top 10 movies in terms of the box office in China in 2018 were women. The proportion of female moviegoers of domestic fantasy  and  each surpassed 60 percent, according to Liu Jia, one of the writers of the report.The stereotype about Chinese women who do not like action or sci-fi films has been broken. Last year, foreign and domestic blockbusters such as  and  have all attracted more female moviegoers than their male counterparts, it said.The report noted that Chinese female viewers' preference was not confined to romantic movies. They also played a leading role in the contribution to the box office for comedies, action, sci-fi and adventure films.The report was released by organizations including China Film Association at the ongoing 22nd Shanghai International Film Festival."
    print(Word(text))





