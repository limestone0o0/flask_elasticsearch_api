from flask import jsonify
from flask_restful import Resource, reqparse
from elasticsearch import Elasticsearch
client = Elasticsearch()


class SearchList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('q', type=str, location='args', required=True)

    def get(self):
        # abort_if_todo_doesnt_exist(t_id)
        key_words = self.parser.parse_args().get('q')

        res = client.search(
            index='jobbole',
            body={
                'query': {
                    'multi_match': {
                        'query': key_words,
                        'fields': ['art_title', 'art_description', 'art_company_name']
                    }
                },
                'from': 0,
                'size': 10,
                'highlight': {
                    'pre_tags': ['<span class="keyword">'],
                    'post_tags': ['</span>'],
                    'fields': {
                        'art_title': {},
                        'art_description': {},
                        'art_company_name': {}
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
            if 'art_description' in hit['highlight']:
                hit_dict['art_description'] = hit['highlight']['art_description'][:50]
            else:
                hit_dict['art_description'] = hit['_source']['art_description'][:50]
            if 'art_company_name' in hit['highlight']:
                hit_dict['art_company_name'] = hit['highlight']['art_company_name']
            else:
                hit_dict['art_company_name'] = hit['_source']['art_company_name']
            hit_dict['create_date'] = hit['_source']['art_time']

            hit_list.append(hit_dict)

        r = {
            'code': '200',
            'total': total_nums,
            'res': hit_list
        }
        return jsonify(r)
