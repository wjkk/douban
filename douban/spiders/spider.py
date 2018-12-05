#!/usr/bin/env python
# encoding: utf-8
"""
@author: chenchuan@autohome.com.cn
@time: 2017/03/13
"""
import random
import string

import scrapy
import requests
import urllib.request
import time
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import Spider
from douban.items import DoubanItem

from scrapy.conf import settings
import pymysql.cursors

domain = 'https://movie.douban.com'


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def complete_url(_url):
    if not _url.startswith('http', 0, 4):
        _url = domain + _url
    return _url


class DoubanSpider(Spider):
    name = 'douban_spider'
    website_possible_httpstatus_list = [200]
    # 已经抓取的item不会重新抓取，故把电影和电视剧摆在最前
    tags = [u'综艺', u'动漫', u'纪录片', u'短片', u'同性', u'歌舞', u'历史', u'西部', u'奇幻', u'冒险',
            u'灾难', u'武侠', u'电视剧', u'电影', u'爱情', u'喜剧', u'动画', u'剧情', u'科幻', u'动作',
            u'经典', u'悬疑', u'青春', u'犯罪', u'惊悚', u'文艺', u'搞笑', u'纪录片', u'励志', u'恐怖',
            u'战争', u'短片', u'黑色幽默', u'魔幻', u'传记', u'情色', u'感人', u'暴力', u'动画短片',
            u'家庭', u'音乐', u'童年', u'浪漫', u'黑帮', u'女性', u'同志', u'史诗', u'童话',
            u'烂片', u'cult', u'脱口秀']

    # tags = [u'电视剧', u'电影']

    def __init__(self):
        host = settings['MYSQL_HOST']
        port = settings['MYSQL_PORT']
        db = settings['MYSQL_DB']
        user = settings['MYSQL_USER']
        password = settings['MYSQL_PASSWORD']
        charset = settings['MYSQL_CHARSET']
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
        self.cursor = self.conn.cursor()
        self.table = settings['MYSQL_TABLE_DOUBAN']

    def start_requests(self):
        while(True):
            # append type
            sql = "select * from `{table}` where get_detail = 0 order by id DESC LIMIT 10000;".format(table=self.table)
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            if rows:
                for row in rows:
                    url = 'https://movie.douban.com/subject/' + str(row[0]) + '/'
                    try:
                        yield Request(url=url, callback=self.parse_item, meta={"check_director": True, "type": row[6],
                                                                   "title": row[1], "tag" : row[20],
                                                                   "score": row[3], "num": row[4],
                                                                   "url": url})
                    except Exception as e:
                        print(e)
                        continue


            else:
                break



    def parse_page(self, response):
        print("parse_page")
        """
        爬取某标签电影分页信息
        """
        hxs = Selector(response)
        total = hxs.xpath('//*[@id="content"]/div/div[1]/div[3]/a[10]/text()').extract()[0]
        tag = response.meta["tag"]
        encoded_tag = format(tag)
        for i in range(int(total)):
            url = complete_url('/tag/{0}?start={1}&type=T'.format(encoded_tag, i * 20))
            yield Request(url=url, callback=self.parse_items, meta={"tag": tag, "check_total": True})

    # 电影详情
    def parse_items(self, response):
        print("parse_items")
        """
        爬取电影链接
        """
        tag = response.meta["tag"]

        try:
            hxs = Selector(response)
            texts = hxs.xpath('//div[contains(@class,"grid-16-8 clearfix")]/div[1]/div[2]/table')
            for text in texts:
                title = text.xpath('tr/td[2]/div/a/text()').extract()
                title = title[0].strip().replace('\n', "").replace(' ', "").replace('/', "") if title else ''
                score = text.xpath('tr/td[2]/div/div/span[2]/text()').extract()
                if score:
                    score = score[0].replace("'", "")
                    if not is_number(score):
                        score = 0
                else:
                    score = 0
                num = text.xpath('tr/td[2]/div/div/span[3]/text()').extract()
                if num:
                    num = num[0].replace('(', "").replace('人评价)', "")
                    if not is_number(num):
                        num = 0
                else:
                    num = 0
                url = text.xpath('tr/td/a/@href').extract()[0]

                item = DoubanItem()
                item['id'] = url.split('/')[-2]
                item['name'] = title
                item['score'] = score
                item['num'] = num
                item['link'] = url
                item['type'] = tag
                item['tag'] = tag
                yield item

                #yield Request(url=url, callback=self.parse_item, meta={"check_director": True, "type": type,
                #                                                       "title": title, "tag" : tag,
                #                                                       "score": score, "num": num,
                #                                                       "url": url})
        except Exception as e:
            print(e)
            pass


    def parse_item(self, response):
        print("parse_item")
        """
        爬取电影信息
        """
        item = DoubanItem()
        directors = ''
        screenwriters = ''
        tags = ''
        actors = ''
        country = ''
        language = ''
        time = ''
        length = ''
        alias = ''
        subtitle = ''
        detail = ''
        longtime = ''
        publish_zone = ''
        avatar = ''
        try:
            title = response.meta["title"]
            score = response.meta["score"]
            num = response.meta["num"]
            url = response.meta["url"]
            hxs = Selector(response)
            # 存储非导演、编剧、主演的属性由哪行开始
            flex_start_row_idx = 3
            try:
                for i in range(3):
                    temp_attr = hxs.xpath('//*[@id="info"]/span[%s]/span[1]/text()' % (i + 1)).extract()[0]
                    if temp_attr == '导演':
                        director_list = hxs.xpath('//*[@id="info"]/span[%s]/span[2]/a/text()' % (i + 1)).extract()
                        directors = ''
                        for director_item in director_list:
                            directors += '/' + director_item

                        directors = directors if directors != '' else '/'
                        directors = directors.split('/', 1)[1]
                    elif temp_attr == '编剧':
                        screenwriter_list = hxs.xpath('//*[@id="info"]/span[%s]/span[2]/a/text()' % (i + 1)).extract()
                        screenwriters = ''
                        for screenwriter_item in screenwriter_list:
                            screenwriters += '/' + screenwriter_item

                        screenwriters = screenwriters if screenwriters != '' else '/'
                        screenwriters = screenwriters.split('/', 1)[1]
                    elif temp_attr == '主演':
                        actor_list = hxs.xpath('//*[@id="info"]/span[%s]/span[2]/a/text()' % (i + 1)).extract()
                        actors = ''
                        for actor_item in actor_list:
                            actors += '/' + actor_item

                        actors = actors if actors != '' else '/'
                        actors = actors.split('/', 1)[1]
                    else:
                        # 非导演、编剧、主演，存储并跳出循环
                        flex_start_row_idx = i
                        break
            except Exception as e:
                print(e)
                # 非导演、编剧、主演，存储并跳出循环
                flex_start_row_idx = i
                pass

            prev_attr_name = ''
            attr = ''
            last_attr = False
            for i in range(flex_start_row_idx, 30):
                try:
                    temp_attr = hxs.xpath('//*[@id="info"]/span[%s]/text()' % (i + 1)).extract()[0]
                    if temp_attr.find(':') != -1:
                        attr = attr if attr != '' else '/'
                        if prev_attr_name == '类型':
                            tags = attr.split('/', 1)[1]
                        #elif prev_attr_name == '制片国家/地区':
                            # publish_zone = attr.split('/', 1)[1]
                        #    print(222)
                        #elif prev_attr_name == '语言':
                         #   language = attr.split('/', 1)[1]
                         #    print(222)
                        elif prev_attr_name == '上映日期':
                            time = attr.split('/', 1)[1]
                        elif prev_attr_name == '首播':
                            time = attr.split('/', 1)[1]
                        #elif prev_attr_name == '片长':
                        #    language = attr.split('/', 1)[1]
                        #    print(222)
                        elif prev_attr_name == '又名':
                            # subtitle = attr.split('/', 1)[1]
                            last_attr = True
                        prev_attr_name = temp_attr.split(':', 1)[0]
                        attr = ''
                    else:
                        attr += '/' + temp_attr
                except Exception as e:
                    print(e)
                    break

                if last_attr:
                    break

            try:
                publish_zone = hxs.xpath('//*[@id="info"]/span[.//text()[normalize-space(.)="制片国家/地区:"]]/following::text()[1]').extract()[0]
            except Exception as e:
                print(e)
            try:
                subtitle = hxs.xpath('//*[@id="info"]/span[.//text()[normalize-space(.)="又名:"]]/following::text()[1]').extract()[0]
            except Exception as e:
                print(e)
            try:
                detail = hxs.xpath('//*[@id="link-report"]/span/text()').extract()[0]
            except Exception as e:
                print(e)

            try:
                avatar = hxs.xpath('//*[@id="mainpic"]/a/img/@src').extract()[0]
            except Exception as e:
                print(e)


            item['id'] = url.split('/')[-2]
            item['name'] = title
            item['score'] = score
            item['num'] = num
            item['link'] = url
            item['directors'] = directors
            item['screenwriters'] = screenwriters
            item['actors'] = actors
            item['tags'] = tags
            item['publish_time'] = time
            item['length'] = length
            item['subtitle'] = subtitle
            item['detail'] = detail.strip()
            item['longtime'] = longtime
            item['publish_zone'] = publish_zone
            item['avatar'] = avatar
            item['type'] = response.meta["tag"]
            item['tag'] = response.meta["tag"]
            item['get_detail'] = 1
            yield item

        except Exception as e:
            print(e)
            pass
