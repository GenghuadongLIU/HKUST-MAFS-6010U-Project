# -*- coding: utf-8 -*-
import scrapy
import os
import re
import requests
from lxml import etree

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

session = requests.Session()

class CogxSpiderSpider(scrapy.Spider):
    name = 'cogx_spider'
    allowed_domains = ['cogx.co']
    start_urls = ['http://cogx.co/']

    def parse(self, response):
        menu_1 = response.xpath('//ul[@id="menu-main-menu"]/li/a/text()').extract()  # name of level_1 menu
        menu_1 = [validateTitle(x) for x in menu_1]
        menu_1_url = response.xpath('//ul[@id="menu-main-menu"]/li/a/@href').extract()  # url of level_1 menu
        if not os.path.exists('D:/Pycodes/cogx/data'):
            os.makedirs('D:/Pycodes/cogx/data')
        # print(menu_1, menu_1_url)
        for each in menu_1:
            if not os.path.exists('D:/Pycodes/cogx/data/' + each):
                os.makedirs('D:/Pycodes/cogx/data/' + each)
            if menu_1_url[menu_1.index(each)] == '#' or menu_1_url[menu_1.index(each)] == 'https://cogx.co/topics/':
                continue
            else:
                # print('-'*30)
                url = menu_1_url[menu_1.index(each)]
                req = session.get(url)
                req.encoding = 'utf8'
                resp = etree.HTML(req.content)
                # print(req.text)
                if url != 'https://cogx.co/tickets/':
                    content = ''.join(resp.xpath('//main//text()'))
                else:
                    content = ''.join(resp.xpath('//div[@class="ticket-grid"]//text()'))
                # print(content)
                with open('D:/Pycodes/cogx/data/' + each + '/' + each + '.txt', 'w', encoding='utf-8') as f:
                    f.write(content)

            if menu_1.index(each) != 0 and menu_1.index(each) != 5:  # there are sub-menus
                menu_2 = response.xpath('//ul[@id="menu-main-menu"]/li[' + str(menu_1.index(each) + 1) + ']/ul[@class="sub-menu"]/li/a/text()').extract()  # name of level_2 menu
                menu_2 = [validateTitle(x) for x in menu_2]
                menu_2_url = response.xpath('//ul[@id="menu-main-menu"]/li[' + str(menu_1.index(each) + 1) + ']/ul[@class="sub-menu"]/li/a/@href').extract()  # url of level_2 menu
                print(menu_2, menu_2_url)
                for each2 in menu_2:
                    print('-' * 30)
                    if not os.path.exists('D:/Pycodes/cogx/data/' + each + '/' + each2):
                        os.makedirs('D:/Pycodes/cogx/data/' + each + '/' + each2)
                    url = menu_2_url[menu_2.index(each2)]
                    req = session.get(url)
                    req.encoding = 'utf8'
                    resp = etree.HTML(req.content)
                    # print(req.text)
                    content = ''.join(resp.xpath('//main//text()'))
                    # print(content)
                    with open('D:/Pycodes/cogx/data/' + each + '/' + each2 + '/' + each2 + '.txt', 'w', encoding='utf-8') as f:
                        f.write(content)



