# coding=utf-8
from elasticsearch import Elasticsearch

class ElasticMaterialObj:

    def __init__(self, index_name, index_type, ip):
        '''
        :param index_name: 索引名
        :param index_type: 索引类型
        :param ip: ip
        '''
        self.index_name = index_name
        self.index_type = index_type
        # 无用户名密码状态
        self.esObj = Elasticsearch([{'host': ip, 'port': 9200}])
        # 用户名密码状态
        # self.esObj = Elasticsearch([ip],http_auth=('elastic', 'password'),port=9200)

    def create_index(self, index_name='resource', index_type='resource_type'):
        '''
        创建索引,默认索引名称为resource，类型为resource_type的索引
        :param index_name:
        :param index_type:
        :return:
        '''
        # 创建索引
        _index_mappings = {
            "mappings": {
                self.index_type: {
                    "dynamic": True,
                    "properties": {
                        "url_object_id": {
                            "type": "keyword",
                        },
                        "url": {
                            "type": "keyword",
                        },
                        "title": {
                            "analyzer": "english",
                            "type": "text",  # keyword不会进行分词,text会分词
                        },
                        "source": {
                            "type": "keyword",
                        },
                        "tags": {
                            "analyzer": "english",
                            "type": "text"
                        },
                        "level": {
                            "type": "integer"
                        },
                        "audio": {
                            "type": "keyword",
                        },
                        "image": {
                            "type": "keyword",
                        },
                        "create_date": {
                            "type": "date",
                        },
                        "teacher_name": {
                            "type": "keyword",
                        },
                        "web_source": {
                            "type": "keyword",
                        },
                        "contents": {
                            "analyzer": "english",
                            "type": "text"
                        },
                    }
                }
            }
        }
        res = self.esObj.indices.create(index=self.index_name, body=_index_mappings)
        print(res)


es = ElasticMaterialObj('subject', 'sub_type', ip='kouxun.lenovoresearch2019.cn')
if es.esObj.indices.exists(index=es.index_name) is True:
    print('index is already exist')
else:
    es.create_index()
    print('index create success')