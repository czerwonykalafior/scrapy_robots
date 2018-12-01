import json

json_mapping = """{
  "id": "loc_id",
  "listingType": "listing",
  "listingModel": {
    "promoType": "promo_type",
    "url": "loc_website",
    "images": [
      "/UAWeWRQqiFT-KU7eVULhRTfWops=/548x365/filters:format(jpeg):quality(80)/w800-h600-2011712479_1_pi_150121_120319"
    ],
    "price": "price",
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
      "street": "address_street",
      "suburb": "address_suburb",
      "state": "address_state",
      "postcode": "address_postcode",
      "lat": "address_lat",
      "lng": "address_lng"
    },
    "features": {
      "parking": "feautures_parking",
      "propertyType": "feautures_property_type",
      "isRural": false,
      "landSize": "feautures_land_size",
      "landUnit": "feautures_land_unit"
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
}"""

import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in '%s': %s" % (cwd, files))

with open('results.json', 'r', encoding='utf-8') as f:
    dict_data = json.load(f)

lat_lng = []
for loc in dict_data:
    try:
        lat = loc['listingModel']['address']['lat']
        lng = loc['listingModel']['address']['lng']
        lat_lng.append((lat, lng))
    except:
        print(loc['listingModel']['address'])


print(lat_lng)

#
# dict_mapping = json.loads(json_mapping)
#
# for key1, val1 in dict_mapping.items():
#     print(key1, val1)
#     print
#     for key2 in dict_mapping[key1]:
#         print('lvl2: ', key2)