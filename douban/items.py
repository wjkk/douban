# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class DoubanItem(Item):
    id = Field()
    name = Field()
    score = Field()
    num = Field()
    link = Field()
    type = Field()
    directors = Field()
    screenwriters = Field()
    actors = Field()
    tags = Field()
    tag = Field()
    publish_time = Field()
    length = Field()
    updated_at = Field()
    created_at = Field()
    subtitle = Field()
    detail = Field()
    longtime = Field()
    publish_zone = Field()
    avatar = Field()
    get_detail = Field()
