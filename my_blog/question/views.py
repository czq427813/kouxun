from django.shortcuts import render,redirect
from elasticsearch import Elasticsearch
import time
import re
#client = Elasticsearch(hosts=["127.0.0.1:9200"])
client = Elasticsearch(hosts=["http://kouxun.lenovoresearch2019.cn:9200"])
sub_id = 0


def question_list(request):
    search = request.GET.get('search')
    source = request.GET.get('source')
    page = request.GET.get('page')
    web_source = request.GET.get('web_source')
    if page:
        page = int(page)
    else:
        page = 1
    question_list = client.search(
        index="subject",
        body={
            "query": {
                "match_all": {}
            },
            "from": (page - 1) * 10,
            "size": 10,
        }
    )
    # 搜索查询集
    if search and search != 'None':
        question_list = client.search(
            index="subject",
            body={
                "query": {
                    "multi_match": {
                        "query": search,
                        "fields": ["title", "content", "tag"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
            }
        )
    else:
        # 将 search 参数重置为空
        search = ''
    # 来源查询集
    if source and source != 'None':
        question_list = client.search(
            index="subject",
            body={
                "query": {
                    "multi_match": {
                        "query": source,
                        "fields": ["source"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
            }
        )

    # 网站来源查询集
    if web_source and web_source != 'None':
        question_list = client.search(
            index="subject",
            body={
                "query": {
                    "multi_match": {
                        "query": web_source,
                        "fields": ["web_source"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
            }
        )
    questions = []
    for hit in question_list["hits"]["hits"]:
        hit_dict = {}
        hit_dict["title"] = hit["_source"]["title"]
        content = ""
        for temp in hit["_source"]["contents"]:
            content += temp
        hit_dict["contents"] = content
        hit_dict["tag"] = hit["_source"]["tag"]
        hit_dict["id"] = hit["_id"]
        hit_dict["create_date"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", hit["_source"]["create_date"]).group(0)
        hit_dict["source"] = hit["_source"]["source"]
        questions.append(hit_dict)

    total_nums = question_list["hits"]["total"]
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
        'questions': questions,
        'search': search,
        'has_previous': has_previous,
        'previous_page_number': previous_page_number,
        'number': number,
        'has_next': has_next,
        'next_page_number': next_page_number,
        'page_nums': page_nums,
        'source': source,
        'web_source': web_source,
    }
    return render(request, 'question/question-list.html', context)


def question_detail(request, id):
    question_list = client.search(
        index="subject",
        body={
            "query": {
                "multi_match": {
                    "query": id,
                    "fields": ["_id"]
                }
            }
        }
    )
    hit_dict = {}
    for hit in question_list["hits"]["hits"]:
        hit_dict["title"] = hit["_source"]["title"]
        hit_dict["contents"] = hit["_source"]["contents"]
        hit_dict["tag"] = hit["_source"]["tag"]
        hit_dict["url_object_id"] = hit["_source"]["url_object_id"]
        hit_dict["id"] = hit["_id"]
    context = {'question': hit_dict}
    return render(request, 'question/detail.html', context)


def question_delete(request, id):
    client.delete(index='subject', doc_type='sub_type', id=id)
    time.sleep(1)
    return redirect("question:question_list")


def question_update(request, id):
    # 获取需要修改的具体文章对象
    all_question = client.search(
        index="subject",
        body={
            "query": {
                "multi_match": {
                    "query": id,
                    "fields": ["_id"]
                }
            }
        }
    )
    question = {}
    url_object_id, url, source, tag, temp_id, web_source = "", "", "", "", "",""
    for hit in all_question["hits"]["hits"]:
        create_date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", hit["_source"]["create_date"]).group(0)
        url = hit["_source"]["url"]
        temp_id = hit["_id"]
        source = hit["_source"]["source"]
        tag = hit["_source"]["tag"]
        web_source = hit["_source"]["web_source"]
        url_object_id = hit["_source"]["url_object_id"]
        question["title"] = hit["_source"]["title"]
        question["contents"] = hit["_source"]["contents"]

    # 判断用户是否为 POST 提交表单数据
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
        client.index(index='subject', doc_type='sub_type', id=temp_id, body=body)
        time.sleep(1)
        return redirect("question:question_detail", id=id)
    else:
        context = {'question': question}
        return render(request, 'question/update.html', context)