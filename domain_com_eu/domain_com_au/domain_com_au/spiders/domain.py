# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin

import scrapy
from bs4 import BeautifulSoup


class DomainSpider(scrapy.Spider):
    name = 'domain'
    allowed_domains = ['domain.com.au']
    start_urls = ['https://www.domain.com.au/Public/SiteMap.aspx']

    def parse(self, response):
        """
        @url https://www.domain.com.au/Public/SiteMap.aspx
        @returns requests 8 16
        """
        # 1) Loop and open links "All .*? Suburbs"
        soup = BeautifulSoup(response.body, 'html.parser')
        region_links = soup.findAll('a', text=re.compile('All.*Suburbs'))

        for link in region_links:
            rel_url = link['href']
            #
            if '/buy/' not in rel_url:
                continue
            yield scrapy.Request(url=urljoin(response.url, rel_url), callback=self.parse_regions)

    def parse_regions(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        suburbs_links = soup.find("ul", class_="suburbs-list")
        suburbs_links = suburbs_links.find_all("a")

        for link in suburbs_links:
            link = link['href']
            self.log(link)
        # 2) Loop over inks in 'ul class="suburbs-list"' and extract < suburb >
        # from links  =  https: // www.domain.com.au / sale / (.* ?) /
        # suburbs = ['acton-act-2601', 'bruce-act-2617']
        #
        # for suburb in suburbs:
        #     url = 'https://www.domain.com.au/sale/api/map-search/?suburb=' \
        #           + suburb + '&sort=price-asc&mode=sale&digitaldata=1&displaymap=1'
        #     yield scrapy.Request(url=url, callback=self.parse_listing)

    def parse_listing(self, response):
        pass
        debug_data = '''[
  {
    "id": 2011712479,
    "listingType": "listing",
    "listingModel": {
      "promoType": "elite",
      "url": "/37-king-sydney-nsw-2000-2011712479",
      "images": [
        "/UAWeWRQqiFT-KU7eVULhRTfWops=/548x365/filters:format(jpeg):quality(80)/w800-h600-2011712479_1_pi_150121_120319"
      ],
      "price": "$105,000",
      "hasVideo": false,
      "branding": {
        "brandLogo": "/HNXS7k1spRABjvvHUXyRcnHPKSs=/117x36/filters:format(jpeg):quality(80)/https://images.domain.com.au/img/Agencys/3375/logo_3375.png",
        "brandName": "John P. Bennetts Real Estate Pty Ltd",
        "brandColor": "#317ab7",
        "agentPhoto": "/mxAQC3ELeMtY8bGWZosbozbz5Ts=/55x55/filters:format(jpeg):quality(80)/https://images.domain.com.au/img/3375/contact_5207.jpeg?mod=180518-130547",
        "agentName": "John Bennetts",
        "agencyId": 3375
      },
      "address": {
        "street": "37 King",
        "suburb": "SYDNEY",
        "state": "NSW",
        "postcode": "2000",
        "lat": -33.8688049,
        "lng": 151.204361
      },
      "features": {
        "parking": 1,
        "propertyType": "CarSpace",
        "isRural": false,
        "landSize": 0,
        "landUnit": "m²"
      },
      "inspection": {
        "inspectionDateTime": null
      },
      "tags": {
        "tagText": null,
        "tagClassName": null
      },
      "shortlist": {
        "shortlisted": false
      }
    }
  },
  {
    "id": 2014787880,
    "listingType": "listing",
    "listingModel": {
      "promoType": "elite",
      "url": "/101-650-george-st-sydney-nsw-2000-2014787880",
      "images": [
        "/VQ-g-Xh-wj9DdFTy8iT8u2_xmC4=/548x365/filters:format(jpeg):quality(80)/2014787880_1_1_181116_030709-w800-h561"
      ],
      "price": "$150,000",
      "hasVideo": false,
      "branding": {
        "brandLogo": "/QSVqqW_hgBOLewxJdgdl_sF01xA=/117x36/filters:format(jpeg):quality(80)/https://images.domain.com.au/img/Agencys/20095/logo_20095.GIF",
        "brandName": "For Sale By Owner Australia",
        "brandColor": "#ffffff",
        "agentPhoto": null,
        "agentName": "For Sale By Owner (NSW)",
        "agencyId": 20095
      },
      "address": {
        "street": "101/650 George St",
        "suburb": "SYDNEY",
        "state": "NSW",
        "postcode": "2000",
        "lat": -33.8769264,
        "lng": 151.20665
      },
      "features": {
        "propertyType": "VacantLand",
        "isRural": false,
        "landSize": 15,
        "landUnit": "m²"
      },
      "inspection": {
        "inspectionDateTime": "2018-12-07T08:30:00"
      },
      "tags": {
        "tagText": null,
        "tagClassName": null
      },
      "shortlist": {
        "shortlisted": false
      }
    }
  },
  {
    "id": 2014666862,
    "listingType": "listing",
    "listingModel": {
      "promoType": "standardpp",
      "url": "/402-219-kent-street-sydney-nsw-2000-2014666862",
      "images": [
        "/uNlvtAYvGwnBVAuq5pzLh_DdPaM=/548x365/filters:format(jpeg):quality(80)/2014666862_1_1_180927_053159-w1600-h1067",
        "/AGdWsBrbqy5vN2KUNqRBkJuSAlo=/548x365/filters:format(jpeg):quality(80)/2014666862_2_1_180927_053159-w1600-h1067",
        "/IAzecdkkmSscaijpu1-FF-j1wYI=/548x365/filters:format(jpeg):quality(80)/2014666862_3_1_180927_053159-w1600-h1067",
        "/_Ff3Ak6n3AZpKQGh9h_cbuAW-9Q=/548x365/filters:format(jpeg):quality(80)/2014666862_4_1_180927_053159-w1600-h1067",
        "/Cnn7W2FQO-Sa30NJBdrx2KFGc6E=/548x365/filters:format(jpeg):quality(80)/2014666862_5_1_180927_053201-w1600-h1067"
      ],
      "price": "$395,000",
      "hasVideo": false,
      "branding": {
        "brandLogo": "/q3X5MURehdFa1ZRQg3WIhK7cD5U=/117x36/filters:format(jpeg):quality(80)/https://images.domain.com.au/img/Agencys/15365/logo_15365.png?date=131749759300060101",
        "brandName": "Century 21 City Quarter",
        "brandColor": "#252527",
        "agentPhoto": "/Vx4fg4gPDYsW84TcwONVh8YE9do=/55x55/filters:format(jpeg):quality(80)/https://images.domain.com.au/img/15365/contact_1393665.jpeg?mod=181127-154605",
        "agentName": "Grant Lee",
        "agencyId": 15365
      },
      "address": {
        "street": "402/219 Kent Street",
        "suburb": "SYDNEY",
        "state": "NSW",
        "postcode": "2000",
        "lat": -33.86481,
        "lng": 151.203735
      },
      "features": {
        "baths": 1,
        "propertyType": "ApartmentUnitFlat",
        "isRural": false,
        "landSize": 0,
        "landUnit": "m²"
      },
      "inspection": {
        "inspectionDateTime": null
      },
      "tags": {
        "tagText": null,
        "tagClassName": null
      },
      "shortlist": {
        "shortlisted": false
      }
    }
  },
  {
    "id": 2014348941,
    "listingType": "listing",
    "listingModel": {
      "promoType": "standardpp",
      "url": "/384-27-park-street-sydney-nsw-2000-2014348941",
      "images": [
        "/S9QGMEzFDw--zWQ1PnD6wOa_SzM=/548x365/filters:format(jpeg):quality(80)/2014348941_1_1_180501_042816-w800-h534",
        "/0sM7b3T3oajj19EAGnqnAZ1vkU0=/548x365/filters:format(jpeg):quality(80)/2014348941_2_1_180501_042817-w800-h534",
        "/27qCUYvmlnyvJOMbHQ6UWmH1zYo=/548x365/filters:format(jpeg):quality(80)/2014348941_3_1_180501_042816-w800-h534",
        "/4nwGVnBhWaAaZce7V2rfxTyDWQg=/548x365/filters:format(jpeg):quality(80)/2014348941_4_1_180501_042817-w800-h534",
        "/rrRbtPMisEQm0O3koKtqx2sH1l8=/548x365/filters:format(jpeg):quality(80)/2014348941_5_1_180501_042816-w800-h534",
        "/eExyyKf9CshnaXOjkz0Do1YJdko=/548x365/filters:format(jpeg):quality(80)/2014348941_6_1_180501_042818-w800-h534"
      ],
      "price": "SOLD  Prior to auction",
      "hasVideo": false,
      "branding": {
        "brandLogo": "/lU9UpAE-Rx6Q73tSerOmA0ZrLC0=/117x36/filters:format(jpeg):quality(80)/https://images.domain.com.au/img/Agencys/11538/logo_11538.png",
        "brandName": "Space Property Agency",
        "brandColor": "#EB5D0B",
        "agentPhoto": "/FYTHyVkMgf9mQ3WLJCTqXeInm2M=/55x55/filters:format(jpeg):quality(80)/https://images.domain.com.au/img/11538/contact_703011.jpeg?mod=180222-152724",
        "agentName": "Conrad Vass",
        "agencyId": 11538
      },
      "address": {
        "street": "384/27 Park Street",
        "suburb": "SYDNEY",
        "state": "NSW",
        "postcode": "2000",
        "lat": -33.8735466,
        "lng": 151.2088
      },
      "features": {
        "baths": 1,
        "propertyType": "Studio",
        "isRural": false,
        "landSize": 0,
        "landUnit": "m²"
      },
      "inspection": {
        "inspectionDateTime": null
      },
      "tags": {
        "tagText": "Under offer",
        "tagClassName": "is-under-offer"
      },
      "shortlist": {
        "shortlisted": false
      }
    }
  }
]'''
