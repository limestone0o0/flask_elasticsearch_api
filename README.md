## elasticsearch_restful_api
### 商城和博客搜索系统api接口开发

开发语言：python
开发框架：flask
开发风格：restful api
开发库：参照requirements.txt

#### 功能
1.提供搜索列表api
2.提供搜索建议api（自带ik分词系统）


#### 安装
pip install -r requirements.txt
设置Elasticsearch并确保它在http：// localhost：9200上运行,linux只能非root用户运行


#### 使用
1.设置Elasticsearch并确保它在http：// localhost：9200上运行
2.在models.py文件中创建你的字段映射
3.首先将mysql数据导入，修改mysql_to_data.py文件中的字段和数据库，也可以从scrapy中导入
  在main中调用你需要插入的函数，其余的函数可以忽略，直接运行同步到es中
4.启动flask


#### 相关接口
1.博客api 'http://127.0.0.1:5000/api/blogslist/ <string:keyword>/<int:page>/<int:limit>'

2.商品api 'http://127.0.0.1:5000/api/bookslist/ <string:keyword>/<int:page>/<int:limit>'

3.搜索建议 'http://127.0.0.1:5000/api/suggest/ <string:types>/<string:keyword>/<int:limit>'

#### api参数
keyword：查询关键词
page：查询页数
limit：每页数据量
type：查询类型（主要针对多个系统查询）

### todo
1.多线程+协程
2.更加精确的搜索建议
3.增量爬虫添加es数据
4.缓存

### 联系
邮箱：xxm13504577723@163.com
欢迎给出建议，欢迎交流，大佬绕道
