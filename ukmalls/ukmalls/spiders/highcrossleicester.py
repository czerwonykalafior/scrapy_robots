# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Selector


class HighcrossleicesterSpider(scrapy.Spider):
    name = 'highcrossleicester'
    allowed_domains = ['highcrossleicester.com']
    start_urls = ['https://www.highcrossleicester.com/visitor-info/contact-us']

    def parse(self, response):
        item = dict()

        item['address1'] = ''.join(Selector(response=response).xpath("//div[@class='column-box']//address//text()").extract()).strip()
        item['phone'] = ''.join(Selector(response=response).xpath('//h2[contains(text(),"Contact")]/following-sibling::*/text()').extract()).strip()

        loc_listing = 'https://www.highcrossleicester.com/ContentPages/Hammerson/Web/ShopGuide.aspx/GetStoreList'

        yield scrapy.Request(url=loc_listing, method='POST', headers={"Content-Type": "application/json"},  body='{"isDining":false}', callback=self.parse_listing, meta={'item': item})

    def parse_listing(self, response):
        item = response.meta['item']
        self.log(response.body)
        json_response = json.loads(response.body)

        for i in json_response['d']:
            item['location'] = i['Location']
            item['loc_name'] = i['Name']
            item['loc_phone'] = i['PhoneNumber']
            item['store_url'] = i['StoreDetailsUrl']
            yield item
