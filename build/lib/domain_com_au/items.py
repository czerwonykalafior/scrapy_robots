# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DomainComAuItem(scrapy.Item):
    loc_id = scrapy.Field()
    price = scrapy.Field()
    loc_name = scrapy.Field()
    address_street = scrapy.Field()
    address_suburb = scrapy.Field()
    address_state = scrapy.Field()
    address_postcode = scrapy.Field()
    address_lat = scrapy.Field()
    address_lng = scrapy.Field()
    feautures_property_type = scrapy.Field()
    feautures_land_size = scrapy.Field()
    feautures_land_unit = scrapy.Field()
    feautures_parking = scrapy.Field()
    feautures_beds = scrapy.Field()
    feautures_baths = scrapy.Field()
    promo_type = scrapy.Field()
    loc_website = scrapy.Field()
