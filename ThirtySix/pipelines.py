# -*- coding: utf-8 -*-
# Author:   BinBin
# Email:    289594665@qq.com
# Time :    2017/07/27

import string
from DBHelper import DBHelper

class ThirtySixPipeline(object):

    def __init__(self):
        self.helper = DBHelper('120.*.215.*', '1433', 'TestForBinBin', 'sa', '******')

    def process_item(self, item, spider):
        print "process_item title" +  item["article_title"]

        #插入数据库的sql语句
        sql = u'insert into T_Article(article_title, article_author, article_url, article_content, article_summary, article_icon) values (\'{t}\',\'{a}\',\'{u}\',\'{c}\',\'{s}\',\'{i}\')'\
            .format(
                t = item["article_title"],
                a = item["article_author"],
                u = item["article_url"],
                c = item["article_content"],
                s = item["article_summary"],
                i = item["article_icon"]
            )
        #这里要特殊处理这个\xa0，是空格，GBK无法转化这个编码
        sql.replace(u'\xa0', u' ')
        row = self.helper.execute(sql.encode('GBK', 'ignore'))
        return item
