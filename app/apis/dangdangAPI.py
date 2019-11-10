from flask import jsonify
from flask_restful import Resource
from elasticsearch import Elasticsearch
client = Elasticsearch()

class SearchShopList(Resource):
    # def __init__(self):
    #     self.parser = reqparse.RequestParser()
    #     self.parser.add_argument('q', type=str, location='args', required=True)

    def get(self, keyword, page, limit):

        limit = int(limit)
        if limit > 20:
            limit = 20
        page = (int(page) - 1) * limit

        key_words = keyword
        res = client.search(
            index='dangdang',
            body={
                'query': {
                    'multi_match': {
                        'query': key_words,
                        'fields': ['title', 'detail_description', 'type', 'author']
                    }
                },
                'from': page,
                'size': limit,
                'highlight': {
                    'pre_tags': ['<span class="keywords">'],
                    'post_tags': ['</span>'],
                    'fields': {
                        'title': {},
                        'detail_description': {},
                        'type': {},
                        'author': {}
                    }
                }
            }
        )
        total_nums = res['hits']['total']
        hit_list = []
        for hit in res['hits']['hits']:
            hit_dict = {}
            if 'title' in hit['highlight']:
                hit_dict['title'] = hit['highlight']['title']
            else:
                hit_dict['title'] = hit['_source']['title']
            if 'author' in hit['highlight']:
                hit_dict['author'] = hit['highlight']['author']
            else:
                hit_dict['author'] = hit['_source']['author']
            hit_dict['publish_time'] = hit['_source']['publish_time']
            hit_dict['price'] = hit['_source']['price']
            hit_dict['picture'] = hit['_source']['picture']
            if 'type' in hit['highlight']:
                hit_dict['type'] = hit['highlight']['type']
            else:
                hit_dict['type'] = hit['_source']['type']
            if 'detail_description' in hit['highlight']:
                hit_dict['detail_description'] = hit['highlight']['detail_description'][:50]
            else:
                hit_dict['detail_description'] = hit['_source']['detail_description'][:50]

            hit_list.append(hit_dict)

        r = {
            'code': '200',
            'total': total_nums,
            'res': hit_list
        }
        return jsonify(r)