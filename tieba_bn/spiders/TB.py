# -*- coding: utf-8 -*-
import json
import re
import time

import scrapy
from lxml import etree
from scrapy import Request

from tieba_bn.global_config import bar_name_list
from tieba_bn.items import TiebaBnItem


class TbSpider(scrapy.Spider):
    name = 'TB'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw={}&ie=utf-8&pn=0'.format(bar_name) for bar_name in bar_name_list]

    @staticmethod
    def datetime2ts(date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M')))

    @staticmethod
    def sub_string(text):
        return re.sub(r'[\t\r ]', '', text)

    def parse(self, response):
        print(response.url)
        html = re.sub(r'(<!--)|(-->)', r'', response.text)
        tree = etree.HTML(html)
        content_url_list = tree.xpath('//a[contains(@href, "/p/")]/@href')
        for content_url in content_url_list:
            yield Request(url='http://tieba.baidu.com' + content_url, callback=self.parse_content)
        try:
            next_page_url = 'https:' + tree.xpath('//a[contains(@class, "next pagination-item")]/@href')[0]
            yield Request(url=next_page_url, callback=self.parse)
        except:
            return

    def parse_content(self, response):
        print('++++++++++++++++++++++++++++++++++++++++++++++++++')
        data_field = json.loads(response.xpath('//div[@data-field]/@data-field').extract_first())
        if data_field['content']['post_no'] == 1:
            pass
        else:
            return
        info = TiebaBnItem()
        bar_name = re.sub(r'[\t\n\a ]', r'', response.xpath('//a[@class="card_title_fname"]//text()').extract_first())
        # print(data_field)
        url = response.url
        print(url)
        title = self.sub_string(response.xpath('//h1[@title]/@title|//h3[@title]/@title').extract_first())
        # print(title)
        tz_id = data_field['content']['post_id']
        # print(tz_id)
        try:
            source = self.sub_string(response.xpath('//a[@class="card_title_fname"]//text()').extract_first())
        except:
            source = ''
        # print(source)
        author = data_field['author']['user_name']
        # print(author)
        try:
            createdate = data_field['content']['date']
        except:
            createdate = response.xpath('//div[@data-field][1]//ul[@class="p_tail"]/li[2]//text()|//div[@class="post-tail-wrap"]/span[last()]//text()').extract_first()
        # print(createdate)
        createdate_timestamp = self.datetime2ts(createdate)
        # print(createdate_timestamp)
        try:
            content = ''.join(re.sub(r'<.*?>', '', self.sub_string(response.xpath('//div[@data-field][1]//div[contains(@id, "post_content")]//text()').extract_first())))
        except:
            content = re.sub(r'<.*?>', '', self.sub_string(data_field['content']['content']))
        # print(content)
        image = response.xpath('//div[@data-field][1]/div[contains(@class, "d_post")]//cc//img/@src').extract()
        # print(image)
        sex = data_field['author'].get('sex', '')
        # print(sex)
        info['bar_name'] = bar_name
        info['url'] = url
        info['title'] = title
        info['tz_id'] = tz_id
        info['source'] = source
        info['author'] = author
        info['create_time_dt'] = createdate
        info['create_time_ts'] = createdate_timestamp
        info['content'] = content
        info['image_url'] = image
        info['gender'] = sex

        html = response.text
        tree = etree.HTML(html)
        reply_floor = tree.xpath('//div[@id="j_p_postlist"]/div')
        reply_li = []
        for each_floor in reply_floor:
            if not each_floor.xpath('.//cc/div'):  # 滤掉百度推广
                return False
            try:
                reply_content = ''.join(each_floor.xpath('//div[@data-field][position()>1]//div[contains(@id, "post_content")]//text()')[0].strip())
            except:
                reply_content = ''
            reply_info = {}
            if len(reply_content) > 0:  # 滤掉无文字的回复
                re_field = each_floor.xpath('./@data-field')[0]
                re_info = json.loads(re_field)
                reply_info['create_date_dt'] = re_info['content'].get('date', '')
                # reply_info['createdate'] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", etree.tostring(each_floor)).group()
                try:
                    reply_info['create_date_ts'] = self.datetime2ts(reply_info['createdate'])
                except BaseException as e:

                    reply_info['create_date_ts'] = ""
                # print "reply_info_createdate_timestamp", reply_info['createdate_timestamp']
                reply_info['author'] = re_info['author']['user_name']
                reply_info['content'] = reply_content
                if reply_info['author'] == info['author']:
                    continue
            if reply_info:
                reply_li.append(reply_info)
        info['project'] = '李映森'

        # info['reply'] = json.dumps(reply_li, ensure_ascii=False)
        print(info)
        # print(info['reply'])
        # yield info