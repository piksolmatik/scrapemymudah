from __future__ import absolute_import

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.starturls import FeedGenerator, FragmentGenerator
from ..utils.processors import Item, Field, Text, Number, Price, Date, Url, Image, Regex
from ..items import PortiaItem, ExtractedDataItem


class MudahGenliststartRegexfollow(BasePortiaSpider):
    name = "h3_mudah_my"
    allowed_domains = [u'www.mudah.my']
    start_urls = [{u'url': u'https://www.mudah.my/Selangor/Properties-for-sale-2001?o=[1-84]&q=&f=p&th=1', # For range use e.g 1 - 82
                   u'fragments': [{u'valid': True,
                                   u'type': u'fixed',
                                   u'value': u'https://www.mudah.my/Selangor/Properties-for-sale-2001?o='},
                                  {u'valid': True,
                                   u'type': u'range',
                                   u'value': u'1-84'}, # For range use e.g 1 - 82
                                  {u'valid': True,
                                   u'type': u'fixed',
                                   u'value': u'&q=&f=p&th=1'}],
                   u'type': u'generated'}]
    rules = [
        Rule(
            LinkExtractor(
                allow=(u'https://www.mudah.my/[\\w+-]+\\.html?$'),
                deny=(u'/honeypot.html')
            ),
            callback='parse_item', #H3: Originally 'parse_item' which is defined in spiders.py
            follow=True
        )
    ]
    #H3:
    #items=[[]] --> Original code structure when exported from Portia, see https://github.com/scrapinghub/portia2code 
    #for how the original parse_item supposed to scrape data
    #For prototype of Item and Field see ..utils.processors
    items = [
        [Item(ExtractedDataItem, None, u'#ContainerMain', [                             #H3:
              Field(u'PageTitle', u'h2.roboto::text', []),                              #Page title
              Field(u'PageURL', []),                                                    #Page source URL - just test for field name to scrape data in spiders.py
              Field(u'OfferPrice', u'dd.dd-price::text', []),                           #Offer price
              Field(u'Location', u'dd.loc_dd::text', []),                               #Location
              Field(u'PropDataList', u'div.highlight-title-value::text', []),           #Property Data (list) 
              Field(u'PropDetailsHeaderList', u'dl.params * dt::text', []),             #Property additional details header (list)
              Field(u'PropDetailsList', u'dl.params * dd::text', []),                   #Property additional details (list)
              Field(u'SellerName', u'div.top_seller_name a::text', []),                 #Seller name
              Field(u'SellerProfileLink', u'div.top_seller_name a::attr(href)', []),    #Seller profile link page
              Field(u'PhoneCarrier', u'div.contact-phone-prefix img::attr(src)', []),   #Seller phone carrier prefix (image's URL)
              Field(u'PhoneNumber', u'div.contact-phone-number img::attr(src)', []),    #Seller phone number (image's URL)
              Field(u'Description', u'p.moreless::text', [])])]                         #Long description text
    ]

