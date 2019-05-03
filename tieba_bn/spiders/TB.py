# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from tieba_bn.global_config import bar_name_list


class TbSpider(CrawlSpider):
    name = 'TB'
    allowed_domains = ['baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw={}&ie=utf-8&pn=0'.format(bar_name) for bar_name in bar_name_list]

    rules = (
        Rule(LinkExtractor(allow=r'&pn=\d+'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
