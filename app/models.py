from elasticsearch_dsl import DocType, Date, Integer, Text, Completion, Keyword
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=['localhost'])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer('ik_max_word', filter=['lowercase'])#大小写转换
class LagouType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    positionId = Keyword()  # 文章id
    art_title = Text(analyzer="ik_max_word")
    art_time = Date()
    art_position = Text(analyzer="ik_max_word")
    art_salary = Text(analyzer="ik_max_word")  # 工资
    art_work_year = Text(analyzer="ik_max_word")  # 要求工作年限
    art_education = Text(analyzer="ik_max_word")  # 学历要求
    art_jobNature = Text(analyzer="ik_max_word")  # 职位类型全职
    company_hitags = Keyword()  # 公司福利
    art_company_name = Text(analyzer="ik_max_word")
    art_company_id = Keyword()

    company_type = Keyword()
    company_size = Keyword()
    company_financestage = Keyword()  # 公司融资轮数
    company_label_list = Keyword()  # 公司吸引力
    art_first_type = Text(analyzer="ik_max_word")  # 具体职位类型
    art_second_type = Text(analyzer="ik_max_word")  # 总体职位类型
    art_third_type = Text(analyzer="ik_max_word")  # 语言职位类型

    compangy_full_position = Text(analyzer="ik_max_word")#具体位置
    art_description = Text(analyzer="ik_max_word")
    fingerprint = Keyword()
    class Meta:
        index = "jobbole"
        doc_type = "article"


class DangDangType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    detail_description = Text(analyzer="ik_max_word")
    picture = Keyword()
    author = Text(analyzer="ik_max_word")
    publish_time = Keyword()
    price = Keyword()
    type = Text(analyzer="ik_max_word")

    class Meta:
        index = "dangdang"
        doc_type = "shops"


class KCType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    art_title = Text(analyzer="ik_max_word")
    art_descriptions = Text(analyzer="ik_max_word")
    art_pic = Keyword()
    art_time = Keyword()
    art_content = Text(analyzer="ik_max_word")

    class Meta:
        index = "kechuang"
        doc_type = "news"


if __name__ == '__main__':
    # LagouType.init()
    # DangDangType.init()
    KCType.init()