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
    name = "dev_mudah_genliststart_regexfollow"
    allowed_domains = [u'www.mudah.my']
    start_urls = [{u'url': u'https://www.mudah.my/Selangor/Properties-for-sale-2001?o=[1-2]&q=&f=p&th=1',
                   u'fragments': [{u'valid': True,
                                   u'type': u'fixed',
                                   u'value': u'https://www.mudah.my/Selangor/Properties-for-sale-2001?o='},
                                  {u'valid': True,
                                   u'type': u'range',
                                   u'value': u'1-2'},
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
    #items = [[]] #Original code when exported from Portia, see https://github.com/scrapinghub/portia2code for how thw original parse_item supposed to scrape data

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        ExtractedDataItem['PageTitle'] = response.xpath('//h2/text()').extract_first()
        ExtractedDataItem['OfferPrice'] = response.xpath('//dd[@class=\'dd-price\']/text()')[1].extract().replace(' ', '')
        ExtractedDataItem['Location'] = response.xpath('//dd[@class=\'loc_dd\']/text()').extract_first()
        return ExtractedDataItem

    #H3: New parsing function utilizing ItemLoader - preferred scraping method - NOT WORKING!
    def new_parse_item(self, response):
        il = ItemLoader(item=ExtractedDataItem(), response=response)
        #il.add_xpath('name', '//div[@class="product_name"]')
        il.add_xpath('PageTitle', '//h2')                                                       #Page title
        il.add_xpath('OfferPrice', '//dd[@class=\'dd-price\']')                                 #Offer price
        il.add_xpath('Location', '//dd[@class=\'loc_dd\']')                                     #Location
        #il.add_xpath('PropDataList', '//div[@class=\'highlight-title-value\']')                 #Property Data (list)
        #il.add_xpath('PropDetailsList', '//dl[@class=\'params\'] // dd')                        #Property additional details (list)
        #il.add_xpath('SellerName', '//div[@class=\'top_seller_name col-xs-8\'] / a')            #Seller name
        #il.add_xpath('SellerProfileLink', '//div[@class=\'top_seller_name col-xs-8\'] / a')     #Seller profile link page
        #il.add_xpath('PhoneCarrier', '//div[@class=\'contact-phone-prefix\'] / img')            #Seller phone carrier prefix (image's URL)
        #il.add_xpath('PhoneNumber', '//div[@class=\'contact-phone-number\'] / img')             #Seller phone number (image's URL)
        #il.add_xpath('Description', '//p[@class=\'moreless\']')                                 #Long description
        #il.load_item()

        #Get the Property category, Area size, no. oh bedrooms and bathrooms



        return ExtractedDataItem

#PropDataList
#PropDataCategory
#PropAreaSize
#PropDataBedroomsCount
#PropDataBathroomsCount
#PropDetailsList
#PropDetailsPropType
#PropDetailsTitleType
#PropDetailsLotType