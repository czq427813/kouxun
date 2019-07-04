#!/usr/bin/python
# -*-encoding=utf-8 -*-


import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings')
django.setup()

from article.models import ArticlePost
from elasticsearch import Elasticsearch
client = Elasticsearch(hosts=["localhost"])


def main():
    query = client.search(
        index="chinadaily",
        body={
            "query": {
                "match_all": {}
            }
        },
        scroll='5m',
        size=100
    )
    results = query['hits']['hits']  # es查询出的结果第一页
    total = query['hits']['total']  # es查询出的结果总量
    scroll_id = query['_scroll_id']  # 游标用于输出es查询出的所有结果
    for i in range(0, int(total / 100) + 1):
        # scroll参数必须指定否则会报错
        query_scroll = client.scroll(scroll_id=scroll_id, scroll='5m')['hits']['hits']
        results += query_scroll
    # Article.objects.all().delete()
    for result in results:
        print('saving article: %s' % result["_source"]["title"])
        article = ArticlePost()
        article.title = result["_source"]["title"]
        article.content = result["_source"]["content"],
        article.save()


if __name__ == '__main__':
    main()
