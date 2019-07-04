from django.shortcuts import render, redirect
from elasticsearch import Elasticsearch
import time
import re

#client = Elasticsearch(hosts=["127.0.0.1:9200"])
client = Elasticsearch(hosts=["http://kouxun.lenovoresearch2019.cn:9200"])


def article_list(request):
    search = request.GET.get('search')
    source = request.GET.get('source')
    tags = request.GET.get('tag')
    page = request.GET.get('page')
    web_source = request.GET.get('web_source')
    if page:
        page = int(page)
    else:
        page = 1
    article_list = client.search(
        index="super_material",
        body={
            "query": {
                "match_all": {}
            },
            "from": (page - 1) * 10,
            "size": 10,
            "sort": "score"
        }
    )
    # 搜索查询集
    if search and search != 'None':
        article_list = client.search(
            index="super_material",
            body={
                "query": {
                    "multi_match": {
                        "query": search,
                        "fields": ["title", "content", "tag"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
                "sort": "score"
            }
        )
    else:
        # 将 search 参数重置为空
        search = ''
    # 来源查询集
    if source and source != 'None':
        article_list = client.search(
            index="super_material",
            body={
                "query": {
                    "multi_match": {
                        "query": source,
                        "fields": ["source"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
                "sort": "score"
            }
        )

        # 标签查询集
    if tags and tags != 'None':
        article_list = client.search(
            index="super_material",
            body={
                "query": {
                    "multi_match": {
                        "query": tags,
                        "fields": ["tag"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
                "sort": "score"
            }
        )
    # 网站来源查询集
    if web_source and web_source != 'None':
        article_list = client.search(
            index="super_material",
            body={
                "query": {
                    "multi_match": {
                        "query": web_source,
                        "fields": ["web_source"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
                "sort": "score"
            }
        )
    articles = []
    for hit in article_list["hits"]["hits"]:
        hit_dict = {}
        hit_dict["title"] = hit["_source"]["title"]
        contents = hit["_source"]["content"]
        hit_dict["content"] = contents.replace('###', '')
        hit_dict["tag"] = hit["_source"]["tag"]
        hit_dict["id"] = hit["_source"]["url_object_id"]
        hit_dict["create_date"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", hit["_source"]["create_date"]).group(0)
        hit_dict["source"] = hit["_source"]["source"]
        articles.append(hit_dict)

    total_nums = article_list["hits"]["total"]
    if (page % 10) > 0:
        page_nums = int(total_nums / 10) + 1
    else:
        page_nums = int(total_nums / 10)
    if page != 1:
        has_previous = True
    else:
        has_previous = False
    if page == 1:
        previous_page_number = 1
    else:
        previous_page_number = page - 1
    number = page
    if page != page_nums:
        has_next = True
    else:
        has_next = False
    if page == page_nums:
        next_page_number = 1
    else:
        next_page_number = page + 1
    context = {
        'articles': articles,
        'search': search,
        'has_previous': has_previous,
        'previous_page_number': previous_page_number,
        'number': number,
        'has_next': has_next,
        'next_page_number': next_page_number,
        'page_nums': page_nums,
        'tag': tags,
        'source': source,
        'web_source': web_source,
    }
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    all_article = client.search(
        index="super_material",
        body={
            "query": {
                "multi_match": {
                    "query": id,
                    "fields": ["url_object_id"]
                }
            }
        }
    )
    hit_dict = {}
    for hit in all_article["hits"]["hits"]:
        hit_dict["title"] = hit["_source"]["title"]
        contents = hit["_source"]["content"].strip()
        content_list = contents.split("###")
        word_normal = []
        for i in content_list:
            j = i.split(" ")
            word_normal.append(j)
        hit_dict["content"] = word_normal
        hit_dict["tag"] = hit["_source"]["tag"]
        hit_dict["id"] = hit["_source"]["url_object_id"]
        hit_dict["web_source"] = hit["_source"]["web_source"]
        superClasswords = []
        for word in hit["_source"]["superclassWord"]:
            superClasswords.append(word)
            superClasswords.append(word.title())
            superClasswords.append(word.upper())
        hit_dict["superclassWord"] = superClasswords
    context = {'articles': hit_dict}
    return render(request, 'article/detail.html', context)


def article_delete(request, id):
    client.delete(index='super_material', doc_type='mate_type', id=id)
    time.sleep(1)
    return redirect("article:article_list")


def article_update(request, id):
    # 获取需要修改的具体文章对象
    all_article = client.search(
        index="super_material",
        body={
            "query": {
                "multi_match": {
                    "query": id,
                    "fields": ["url_object_id"]
                }
            }
        }
    )
    article = {}
    url_object_id, url, source, tag, web_source = "", "", "", "", ""
    for hit in all_article["hits"]["hits"]:
        create_date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", hit["_source"]["create_date"]).group(0)
        url = hit["_source"]["url"]
        source = hit["_source"]["source"]
        tag = hit["_source"]["tag"]
        web_source = hit["_source"]["web_source"]
        url_object_id = hit["_source"]["url_object_id"]
        article["title"] = hit["_source"]["title"]
        temp = hit["_source"]["content"].strip()
        contents = []
        for content in temp.split("###"):
            if content != ' 'and len(content) != 0:
                contents.append(content)
        article["content"] = contents
    # all_question = client.search(
    #     index="subject",
    #     body={
    #         "query": {
    #             "multi_match": {
    #                 "query": id,
    #                 "fields": ["url_object_id"]
    #             }
    #         }
    #     }
    # )
    # question_ids = []
    # for question_id in all_question["hits"]["hits"]:
    #     question_ids.append(question_id["_id"])
    if request.method == "POST":
        content_list1 = request.POST['content'].split("\n")
        content_list2 = []
        for content_temp in content_list1:
            if len(content_temp.strip()):
                content_list2.append(content_temp.strip())
        body = {
            "title": request.POST['title'],
            "contents": content_list2,
            "create_date": create_date,
            "url": url,
            "source": source,
            "tag": tag,
            "url_object_id": url_object_id,
            "web_source": web_source,
        }
        client.index(index='subject', doc_type='sub_type', body=body)
        time.sleep(1)
        return redirect("article:article_detail", id=id)
    else:
        context = {'article': article}
        return render(request, 'article/update.html', context)
