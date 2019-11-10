from flask import jsonify
from flask_restful import Resource
from elasticsearch import Elasticsearch
client = Elasticsearch()

class SearchInfoList(Resource):
    # def __init__(self):
    #     '''
    #     添加get参数，restful不适用
    #     '''
    #     self.parser = reqparse.RequestParser()
    #     self.parser.add_argument('q', type=str, location='args', required=True)

    def get(self, keyword, page, limit):

        limit = int(limit)
        if limit > 20:
            limit = 20
        page = (int(page) - 1) * limit

        # key_words = self.parser.parse_args().get('q')
        key_words = keyword
        res = client.search(
            index='kechuang',
            body={
                'query': {
                    'multi_match': {
                        'query': key_words,
                        'fields': ['art_title', 'art_descriptions', 'art_content']
                    }
                },
                'from': page,
                'size': limit,
                'highlight': {
                    'pre_tags': ['<span class="keywords">'],
                    'post_tags': ['</span>'],
                    'fields': {
                        'art_title': {},
                        'art_descriptions': {},
                        'art_content': {},
                    }
                }
            }
        )
        total_nums = res['hits']['total']
        hit_list = []
        for hit in res['hits']['hits']:
            hit_dict = {}
            if 'art_title' in hit['highlight']:
                hit_dict['art_title'] = hit['highlight']['art_title']
            else:
                hit_dict['art_title'] = hit['_source']['art_title']
            if 'art_content' in hit['highlight']:
                hit_dict['art_content'] = hit['highlight']['art_content']
            else:
                hit_dict['art_content'] = hit['_source']['art_content']
            hit_dict['art_time'] = hit['_source']['art_time']
            hit_dict['art_pic'] = hit['_source']['art_pic']
            if 'art_descriptions' in hit['highlight']:
                hit_dict['art_descriptions'] = hit['highlight']['art_descriptions'][:50]
            else:
                hit_dict['art_descriptions'] = hit['_source']['art_descriptions'][:50]

            hit_list.append(hit_dict)

        r = {
            'code': '200',
            'total': total_nums,
            'res': hit_list
        }
        return jsonify(r)

