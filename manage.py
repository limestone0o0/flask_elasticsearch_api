from app import create_app
from flask_restful import Api
from app.apis.dangdangAPI import SearchShopList
from app.apis.kechuangAPI import SearchInfoList
from app.apis.lagouAPI import SearchList
from app.apis.suggestions import SearchSuggest

app = create_app()
api = Api(app)

api.add_resource(SearchList, '/api/lagoulist/')#测试uri

api.add_resource(SearchInfoList, '/api/blogslist/<string:keyword>/<int:page>/<int:limit>')
api.add_resource(SearchShopList, '/api/bookslist/<string:keyword>/<int:page>/<int:limit>')
api.add_resource(SearchSuggest, '/api/suggest/<string:types>/<string:keyword>/<int:limit>')

from app.main.views import *
if __name__ == '__main__':
    app.run()
