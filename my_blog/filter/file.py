# coding=utf-8
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from filter.Superclass_words import Word
from filter.wordRefind import main
#client = Elasticsearch(hosts=["127.0.0.1:9200"])
client = Elasticsearch(hosts=["http://kouxun.lenovoresearch2019.cn:9200/"])

def article(index_name, index_name1, index_type1):
    query = client.search(
        index=index_name,
        body={
            "query": {
                "match_all": {}
            }
        },
        scroll='3m',
        size=100
    )
    results = query['hits']['hits']  # es查询出的结果第一页
    total = query['hits']['total']  # es查询出的结果总量
    scroll_id = query['_scroll_id']  # 游标用于输出es查询出的所有结果
    for i in range(0, int(total / 100) + 1):
        # scroll参数必须指定否则会报错
        query_scroll = client.scroll(scroll_id=scroll_id, scroll='5m')['hits']['hits']
        results += query_scroll
    actions = []
    scores = {}
    temp = 0
    for result in results:
        temp += 1
        print(result["_source"]["title"])
        text = result["_source"]["content"]
        content_list = text.split("###")
        web_source = result["_index"]
        word = []
        for i in content_list:
            j = i.split(" ")
            word.append(j)
        number = len(word)
        if len(text) >= 400 and len(text)< 3000:
            spuerWrod = Word(text)
            superWords = []
            for k, _ in spuerWrod["superclassWord"].items():
                superWords.append(k)
            score = spuerWrod["num"] / number
            # super_words = {}
            # for word in words:
            #     print(word)
            #     try:
            #         super_words[word] = main(word)
            #     except Exception as e:
            #         pass
            #     print(super_words)
            action = {
                "_index": index_name1,
                "_type": index_type1,
                "_id": result["_id"],
                "_source": {
                    "title": result["_source"]["title"],
                    "create_date": result["_source"]["create_date"],
                    "content": result["_source"]["content"],
                    "url": result["_source"]["url"],
                    "source": result["_source"]["source"],
                    "tag": result["_source"]["tag"],
                    "web_source": web_source,
                    "url_object_id": result["_source"]["url_object_id"],
                    "score": score,
                    "superclassWord": superWords
                    #"wordRefind": super_words
                }
            }
            actions.append(action)
        if temp % 100 == 0:
            helpers.bulk(client, actions)
            actions = []


if __name__ == "__main__":
    article("chinadaily", "super_material", "mate_type")
    # article("51english", "super_material", "mate_type")
    # article("chinaplus", "super_material", "mate_type")