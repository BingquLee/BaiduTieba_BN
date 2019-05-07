# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

from elasticsearch import Elasticsearch

from tieba_bn.items import TiebaBnItem
from tieba_bn.settings import ES_HOST, ES_PORT


class TiebaBnPipeline(object):

    es = Elasticsearch(hosts=[{'host': ES_HOST, 'port': ES_PORT}])

    def process_item(self, item, spider):
        if isinstance(item, TiebaBnItem):
            item_id = dict(item)['url']
            item['update_dt'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item['update_ts'] = int(time.time())
            self.es.index(index='tieba_bn', doc_type='text', id=item_id, body=dict(item))