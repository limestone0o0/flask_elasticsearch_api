import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.models import DangDangType, KCType
from elasticsearch_dsl.connections import connections

# es = connections.create_connection(DangDangType._doc_type.using)
es = connections.create_connection(KCType._doc_type.using)

db = sqlalchemy.create_engine("mysql+pymysql://root:7890@localhost:3306/kechuangdata")

base = declarative_base(db)

class User(base):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(255))
    detail_description = sqlalchemy.Column(sqlalchemy.String(1024))
    picture = sqlalchemy.Column(sqlalchemy.String(255))
    author = sqlalchemy.Column(sqlalchemy.String(255))
    publish_time = sqlalchemy.Column(sqlalchemy.String(255))
    price = sqlalchemy.Column(sqlalchemy.String(10))
    type_id = sqlalchemy.Column(sqlalchemy.Integer)

class User2(base):
    __tablename__ = 'article'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    art_title = sqlalchemy.Column(sqlalchemy.String(100))
    art_descriptions = sqlalchemy.Column(sqlalchemy.Text)
    art_pic = sqlalchemy.Column(sqlalchemy.String(200))
    art_time = sqlalchemy.Column(sqlalchemy.String(30))
    art_url = sqlalchemy.Column(sqlalchemy.String(200))
    art_content = sqlalchemy.Column(sqlalchemy.Text)


def gen_suggest(index, info_tuple):
#根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            #调用es接口分析字符串
            words = es.indices.analyze(index=index, analyzer='ik_max_word',params={'filter':['lowercase']}, body=text)
            anylyzed_words = set([r['token'] for r in words['tokens'] if len(r['token'])>1])
            news_words = anylyzed_words - used_words
        else:
            news_words = set()
        if news_words:
            suggests.append({'input': list(news_words),'weight': weight})
    return suggests

#todo:多线程加协程
def insert_data():
    session = sessionmaker(bind=db)
    session = session()
    temp = ['图形图像多媒体',
            '程序设计',
            '网络与数据通信',
            '数据库',
            '家庭与办公室用书',
            '操作系统/系统开发',
            '信息安全',
            'CAD CAM CAE',
            '软件工程/开发项目管理',
            '计算机考试认证',
            '行业软件及应用',
            '项目管理IT人文',
            '企业软件开发与实施',
            '硬件外部设备维修',
            '影印版',
            '计算机体系结构',
            '计算机理论',
            '电脑杂志——合订本',
            '数码全攻略',
            '计算机教材',
            '人工智能',
            '移动开发',
            '管理信息系统(MIS)',
            '地理信息管理系统（GIS)',
            '英文原版书-计算机']
    type_dict = {}
    for i in range(1,26):
        type_dict[str(i)] = temp[i-1]
    data = session.query(User).all()
    for i in data:
        shops = DangDangType()
        shops.title = i.title
        shops.price = i.price
        shops.author = i.author
        shops.picture = i.picture
        shops.publish_time = i.publish_time
        shops.detail_description = i.detail_description
        shops.type = type_dict[str(i.type_id)]
        shops.suggest = gen_suggest(DangDangType._doc_type.index, ((shops.title, 10), (shops.type, 9),
                                                                   (shops.detail_description, 8),(shops.author, 7),
                                                                   ))
        shops.save()
# data = session.query(User).get(ident=10)

    session.close()


def insert_news():
    session = sessionmaker(bind=db)
    session = session()

    data = session.query(User2).all()
    for i in data:
        shops = KCType()
        shops.art_title = i.art_title
        shops.art_descriptions = i.art_descriptions
        shops.art_pic = i.art_pic
        shops.art_time = i.art_time
        shops.art_content = i.art_content
        shops.suggest = gen_suggest(KCType._doc_type.index, ((shops.art_title, 10), (shops.art_descriptions, 9),
                                                                   (shops.art_content, 8)
                                                                   ))
        shops.save()
    # data = session.query(User).get(ident=10)

    session.close()

if __name__ == '__main__':

    insert_news()
