# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TiebaBnItem(scrapy.Item):
    keyword = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    tz_id = scrapy.Field()
    source = scrapy.Field()
    author = scrapy.Field()
    create_time_dt = scrapy.Field()
    create_time_ts = scrapy.Field()
    content = scrapy.Field()
    image_url = scrapy.Field()
    gender = scrapy.Field()
    reply = scrapy.Field()
    update_dt = scrapy.Field()
    update_ts = scrapy.Field()
    project = scrapy.Field()
    bar_name = scrapy.Field()
