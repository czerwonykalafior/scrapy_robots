# -*- coding: utf-8 -*-
from datetime import date

from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from urllib.parse import urlparse


class SerpentineGreenSpider(CrawlSpider):
    name = 'thegalleria'
    allowed_domains = ['thegalleria.co.uk', 'o2centre.co.uk']
    start_urls = [
        'https://thegalleria.co.uk/shops',
        'https://o2centre.co.uk/shops'
    ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[contains(@class, 'cp_ShopLink')]"), callback='parse_details', follow=True),
    )

    # def parse_start_url(self, response):
    #     address = Selector(response=response).xpath('//div[@class = "address"]').extract()[0]
    #     address = Selector(text=address).xpath('//div[@class = "address__line"]').extract()
    #
    #     item = {}
    #     for n in range(len(address)):
    #         key = 'address' + str(n+1)
    #         item[key] = address[n]
    #     yield item

    def parse_details(self, response):
        selectors = {
            'loc_name': "//h1[@itemprop='name']//text()",
            'location': "//a[@id='centre-map']/@data-floor",
            'loc_website': "//a[contains(@class, 'infoIcon--website')]/@href",
            'phone': "//a[contains(@class,'infoIcon--phone')]//text()",
            'hours_of_operations': "//div[contains(@class,'openingHours')]//text"
        }

        item = dict()
        item['eid'] = self.settings['EXECUTIONID']

        item['datafeed'] = urlparse(response.url).netloc
        item['source_url'] = response.url

        for field, selector in selectors.items():
            item[field] = Selector(response=response).xpath(selector).extract_first()

        yield item
