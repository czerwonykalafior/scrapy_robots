# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider

from urllib.parse import urljoin

import json
import re
from bs4 import BeautifulSoup


class DomainSpider(scrapy.Spider):

    name = 'domain'
    allowed_domains = ['domain.com.au']
    start_urls = ['https://www.domain.com.au/Public/SiteMap.aspx']

    def parse(self, response):
        """
        1) Loop and open links "All .*? Suburbs" in https://www.domain.com.au/Public/SiteMap.aspx/

        @url https://www.domain.com.au/Public/SiteMap.aspx
        @returns requests 8 16
        """

        # E.g:. debug_region='All SA Suburbs'
        debug_region = getattr(self, 'debug_region', None)

        soup = BeautifulSoup(response.body, 'html.parser')

        if debug_region is not None:
            # TODO: TypeError no handled
            pattern = debug_region
        else:
            pattern = 'All.*Suburbs'
        region_links = soup.findAll('a', text=re.compile(pattern))

        for link in region_links:
            rel_url = link['href']
            # TODO: replace hardcoded '/buy/' in link, what if we want to scrape more in future? Replace with -a ?
            if '/buy/' not in rel_url:
                continue
            # TODO: response.follow can be used to skip urljoin with relative URLS
            yield scrapy.Request(url=urljoin(response.url, rel_url), callback=self.parse_regions)

    def parse_regions(self, response):
        """
        2) Loop over links in 'ul class="suburbs-list"'
        and extract <suburb> from links  =  https://www.domain.com.au/sale/(.*?)/

        @url https://www.domain.com.au/real-estate/buy/nsw/
        @returns requests 4800

        """

        # E.g:. debug_suburb_code='port-pirie-sa-5540'
        debug_suburb_code = getattr(self, 'debug_suburb_code', None)

        if debug_suburb_code is not None:
            pattern = '(' + debug_suburb_code + ')'
        else:
            pattern = '/sale/(.*)/'

        soup = BeautifulSoup(response.body, 'html.parser')
        suburbs_links = soup.find("ul", class_="suburbs-list")
        suburbs_links = suburbs_links.find_all("a")

        for link in suburbs_links:
            suburb = re.search(pattern, link['href'], re.IGNORECASE)
            # TODO: Lazy regex error handling
            if suburb:
                suburb = suburb.group(1)
            else:
                continue

            url = 'https://www.domain.com.au/sale/api/map-search/?suburb=' + suburb \
                  + '&sort=price-asc&mode=sale&digitaldata=1&displaymap=1'

            yield scrapy.Request(url=url, callback=self.parse_listing)

    def parse_listing(self, response):
        """
        Extract data from JSON response. Max no of location per 1 page returned = 200

        @url https://www.domain.com.au/sale/api/map-search/?suburb=east-wardell-nsw-2477&sort=price-asc&mode=sale&digitaldata=1&displaymap=1
        @returns items 4 8
        """

        data = json.loads(response.body)

        search_type = data['digitalData']['searchLocationCat']
        if search_type != 'Suburb':
            raise StopIteration

        no_of_locs_found = data['digitalData']['searchResultCount']

        if no_of_locs_found > 400 and '&bedrooms=' in response.url:
            raise CloseSpider(reason='Too much data in response')

        # TODO: Below execution flow has a strong unpleasant smell

        # When more than 400 we have to Filter by no. of bedrooms
        if no_of_locs_found > 400 and '&bedrooms=' not in response.url:
            bedrooms_no_params = ['0', '1', '2', '3', '4', '5-any']
            for no_of_bedrooms in bedrooms_no_params:
                url = response.url + '&bedrooms=' + no_of_bedrooms
                yield scrapy.Request(url=url, callback=self.parse_listing)

        # Max loc on one page is 200. When there is more than 200 loc on listing changing sorting to DESC
        elif no_of_locs_found > 200 and 'price-asc' in response.url:
            for loc in data['results']:
                yield loc

            url = response.url.replace('sort=price-asc', 'sort=price-desc')
            yield scrapy.Request(url=url, callback=self.parse_listing)

        else:
            # TODO: Map Json to columns or store in MongoDB
            for loc in data['results']:
                yield loc
