import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATICFILES_DIR = os.path.join(BASE_DIR, "static")

class Develop(object):
    DEBUG = True
    SECRET_KEY = "debug"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:7890@39.107.253.135:33060/myblog?charset=utf8'  # 数据库地址 sqllite
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 请求结束后自动提交
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # flask1版本之后，添加的选项，目的是跟踪修改


class Test(object):
    TEST = True
    SECRET_KEY = "test"


class Release(object):
    SECRET_KEY = "Release"