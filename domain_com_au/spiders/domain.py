# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider

from urllib.parse import urljoin

import json
import re
from bs4 import BeautifulSoup


class DomainSpider(scrapy.Spider):
    # This design will only work when on the listing page there is less than 400 locations found

    name = 'domain'
    allowed_domains = ['domain.com.au']
    start_urls = ['https://www.domain.com.au/Public/SiteMap.aspx']

    def parse(self, response):
        """
        1) Loop and open links "All .*? Suburbs" in https://www.domain.com.au/Public/SiteMap.aspx/

        @url https://www.domain.com.au/Public/SiteMap.aspx
        @returns requests 8 16
        """

        soup = BeautifulSoup(response.body, 'html.parser')
        region_links = soup.findAll('a', text=re.compile('All.*Suburbs'))

        for link in region_links:
            rel_url = link['href']
            # TODO: replace hardcoded '/buy/' in link, what if we want to scrape more in future?
            if '/buy/' not in rel_url:
                continue
            yield scrapy.Request(url=urljoin(response.url, rel_url), callback=self.parse_regions)

    def parse_regions(self, response):
        """
        2) Loop over links in 'ul class="suburbs-list"'
        and extract <suburb> from links  =  https://www.domain.com.au/sale/(.*?)/

        @url https://www.domain.com.au/real-estate/rent/act/
        @returns requests 130
        """

        soup = BeautifulSoup(response.body, 'html.parser')
        suburbs_links = soup.find("ul", class_="suburbs-list")
        suburbs_links = suburbs_links.find_all("a")

        for link in suburbs_links:
            suburb = re.search('/sale/(.*)/', link['href'], re.IGNORECASE)
            # TODO: Lazy error handling
            suburb = suburb.group(1) if suburb else ''

            url = 'https://www.domain.com.au/sale/api/map-search/?suburb=' + suburb \
                  + '&sort=price-asc&mode=sale&digitaldata=1&displaymap=1'

            yield scrapy.Request(url=url, callback=self.parse_listing)

    def parse_listing(self, response):
        """
        Extract data from JSON response

        @url https://www.domain.com.au/sale/api/map-search/?suburb=sydney-nsw-2000&sort=price-asc&mode=sale&digitaldata=1&displaymap=1
        @returns items 200
        """

        data = json.loads(response.body)

        search_type = data['digitalData']['searchLocationCat']
        if search_type != 'Suburb':
            raise StopIteration

        locs_found = data['digitalData']['searchResultCount']

        # TODO: FAILED. Filter by no. of bedrooms
        if locs_found > 400:
            raise CloseSpider(reason='Too much data in response')

        # Max loc on one page is 200. When there is more than 200 loc on listing changing sorting to DESC
        # TODO: change to : 200 < locs_found < 400
        elif locs_found > 200 and 'price-asc' in response.url:
            url = response.url.replace('sort=price-asc', 'sort=price-desc')
            yield scrapy.Request(url=url, callback=self.parse_listing)

        # TODO: Map Json to columns or store in MongoDB
        for loc in data['results']:
            yield loc
