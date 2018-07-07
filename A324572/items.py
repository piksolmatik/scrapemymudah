from __future__ import absolute_import

import scrapy
from collections import defaultdict
from scrapy.loader.processors import Join, MapCompose, Identity
from w3lib.html import remove_tags
from .utils.processors import Text, Number, Price, Date, Url, Image


class PortiaItem(scrapy.Item):
    fields = defaultdict(
        lambda: scrapy.Field(
            input_processor=Identity(),
            output_processor=Identity()
        )
    )

    def __setitem__(self, key, value):
        self._values[key] = value

    def __repr__(self):
        data = str(self)
        if not data:
            return '%s' % self.__class__.__name__
        return '%s(%s)' % (self.__class__.__name__, data)

    def __str__(self):
        if not self._values:
            return ''
        string = super(PortiaItem, self).__repr__()
        return string


class ExtractedDataItem(PortiaItem):
    #PageTitle
    PageTitle = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),      
    )  
    #PageURL
    PageURL = scrapy.Field(
        input_processor=Url(),
        output_processor=Join(),      
    ) 
    #OfferPrice
    OfferPrice = scrapy.Field(
        input_processor=Text(), #Changed from Price to Text
        output_processor=Join(),
    )
    #Location 
    Location = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )   
    #SellerName     
    SellerName = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )        
    #SellerProfileLink   
    SellerProfileLink = scrapy.Field(
        input_processor=Url(),
        output_processor=Join(),
    )   
    #PhoneCarrier        
    PhoneCarrier = scrapy.Field(
        input_processor=Image(),
        output_processor=Join(),
    )   
    #PhoneNumber       
    PhoneNumber = scrapy.Field(
        input_processor=Image(),
        output_processor=Join(),
    )     
    #Description            
    Description = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    #PropDataList 
    PropDataList = scrapy.Field(
        input_processor=Identity(),     #Originally Text()
        output_processor=Identity(),    #Originally Join()
    )
        #PropDataCategory
    PropDataCategory = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
        #PropAreaSize
    PropAreaSize = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
        #PropDataBedroomsCount
    PropDataBathroomsCount = scrapy.Field(
        input_processor=Number(),
        output_processor=Join(),
    )
        #PropDataBathroomsCount
    PropDataBedroomsCount = scrapy.Field(
        input_processor=Number(),
        output_processor=Join(),
    )
    #PropDetailsHeaderList
    PropDetailsHeaderList = scrapy.Field(
        input_processor=Identity(),     #Originally Text()
        output_processor=Identity(),    #Originally Join()
    )
    #PropDetailsList 
    PropDetailsList = scrapy.Field(
        input_processor=Identity(),     #Originally Text()
        output_processor=Identity(),    #Originally Join()
    )
        #PropDetailsPropType
    PropDetailsPropType = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
        #PropDetailsTitleType
    PropDetailsTitleType = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
        #PropDetailsLotType
    PropDetailsLotType = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
