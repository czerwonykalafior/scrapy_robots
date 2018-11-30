1) Loop and open links "All .*? Suburbs" in https://www.domain.com.au/Public/SiteMap.aspx/ 
2) Loop over links in <ul class="suburbs-list"> and extract <suburb> from links  =  https://www.domain.com.au/sale/(.*?)/
3) Open URL:
https://www.domain.com.au/sale/api/map-search/?suburb=<suburb>&sort=price-asc&mode=sale&digitaldata=1&displaymap=1


IF in JSON value :
searchResultCount: 23,

if searchResultCount > 400 
    than raise HUGE error because this whole idea will fail

if searchResultCount > 200:
    change sorting
    &sort=price-desc

https://www.domain.com.au/sale/api/map-search/?suburb=sydney-nsw-2000&sort=price-asc&mode=sale&digitaldata=1&displaymap=1

https://www.domain.com.au/sale/api/map-search/?suburb=sydney-nsw-2000&sort=price-desc&mode=sale&digitaldata=1&displaymap=1
