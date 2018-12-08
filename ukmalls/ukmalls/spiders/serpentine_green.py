# -*- coding: utf-8 -*-
from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from urllib.parse import urlparse

# Rule(LinkExtractor(restrict_xpaths="//div[contains(@class,'retailer-logo')]"), callback='parse_details', follow=True)
# 'serpentine-green.com','
# 'https://www.serpentine-green.com/shops',


class SerpentineGreenSpider(CrawlSpider):
    name = 'serpentine_green'
    allowed_domains = ['serpentine-green.com', 'beaumontshoppingcentre.com', 'surreyquays.co.uk', 'edenwalkshopping.co.uk']
    start_urls = [
            'https://www.serpentine-green.com/shops',
        'https://www.beaumontshoppingcentre.com/shops',
        'https://www.surreyquays.co.uk/shops',
        'https://www.edenwalkshopping.co.uk/shops'
    ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[contains(text(),'Load More')]"), callback='parse', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[contains(@class,'retailer-logo')]"), callback='parse_details', follow=True)
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
            'loc_name': "//h1[@class='title']//text()",
            'location': "//div[contains(@class, 'field-outlet-location')]//text()",
            'loc_website': "//div[contains(@class,'retailer-website')]//text()",
            'phone': "//div[contains(@class,'-telephone')]//text()",
        }

        item = dict()

        item['datafeed'] = urlparse(response.url).netloc
        item['source_url'] = response.url

        for field, selector in selectors.items():
            item[field] = Selector(response=response).xpath(selector).extract_first()

        yield item
