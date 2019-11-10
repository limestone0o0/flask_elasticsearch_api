from flask import jsonify
from flask_restful import Resource
from elasticsearch import Elasticsearch
client = Elasticsearch()

types_dic = {
    'LGS': 'jobbole',
    'DDS': 'dangdang',
    'KCS': 'kechuang',
}


def get_data(types, words, limit, flag=1):
    limit = int(limit)
    if limit <= 0:
        limit = 6
    if limit > 10:
        limit = 10
    res_list = []
    s = client.search(
        index=types_dic[types],
        body={
            "suggest": {
                "mysuggest": {
                    "text": words,
                    "completion": {
                        "field": "suggest",
                        "fuzzy": {
                            "fuzziness": flag,
                            # 'prefix_length': 0
                        },
                        'size': limit
                    }
                }
            }
        })
    t = s['suggest']['mysuggest'][0]['options']
    for i in t:
        if types_dic[types] == 'dangdang':
            source = i['_source']['title']
        else:
            source = i['_source']['art_title']
        res_list.append(source)
    return res_list


class SearchSuggest(Resource):
    '''
    提供搜索建议
    :return 返回json
    '''
    def get(self, types, keyword, limit):
        words = str(keyword)

        if words:
            res = get_data(types, words, limit)
            if len(res) < limit:
                res2 = get_data(types, words, limit, flag=2)
                res_list = res + res2
            else:
                res_list = res
            if len(res_list) < limit:
                res3 = get_data(types, words, limit, flag=3)
                res_list = res_list + res3

            r = {
                'code': '200',
                'res': res_list[:limit]
            }

            return jsonify(r)
