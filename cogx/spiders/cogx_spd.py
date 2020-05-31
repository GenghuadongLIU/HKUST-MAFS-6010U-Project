# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import os


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


class CogxSpdSpider(CrawlSpider):
    name = 'cogx_spd'
    allowed_domains = ['cogx.co']
    start_urls = ['http://cogx.co/']

    rules = (
        Rule(LinkExtractor(allow_domains='cogx.co'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        content = response.xpath('//main//text()').extract()
        if not content:
            content = response.xpath('//div[@class="container"]//text()').extract()
        # print(content)
        text = ''.join(content)
        curr_url = response.request.url[:-1]
        ref_url = response.request.headers.get('Referer', None)[:-1].decode()
        # print(curr_url, ref_url)
        up = validateTitle(ref_url.split('/')[-2] + '_' + ref_url.split('/')[-1])
        down = validateTitle(curr_url.split('/')[-2] + '_' + curr_url.split('/')[-1])
        file_name = up + '@' + down + '.txt'

        with open('D:/Pycodes/cogx/data/' + validateTitle(file_name), 'w', encoding='utf-8') as f:
            f.write(text)
