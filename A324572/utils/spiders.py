from scrapy.spiders import CrawlSpider
from scrapy.loader import ItemLoader
from scrapy.utils.response import get_base_url

from .starturls import FeedGenerator, FragmentGenerator
from ..items import PortiaItem, ExtractedDataItem #For Test

class RequiredFieldMissing(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class PortiaItemLoader(ItemLoader):
    def get_value(self, value, *processors, **kw):
        required = kw.pop('required', False)
        val = super(PortiaItemLoader, self).get_value(value, *processors, **kw)
        if required and not val:
            raise RequiredFieldMissing(
                'Missing required field "{value}" for "{item}"'.format(
                    value=value, item=self.item.__class__.__name__))
        return val


class BasePortiaSpider(CrawlSpider):
    items = []

    def start_requests(self):
        for url in self.start_urls:
            if isinstance(url, dict):
                type_ = url['type']
                if type_ == 'generated':
                    for generated_url in FragmentGenerator()(url):
                        yield self.make_requests_from_url(generated_url)
                elif type_ == 'feed':
                    yield FeedGenerator(self.parse)(url)
            else:
                yield self.make_requests_from_url(url)

    def parse_item(self, response):
        for sample in self.items:
            items = []
            try:
                for definition in sample:
                    items.extend(
                        [i for i in self.load_item(definition, response)]
                    )
            except RequiredFieldMissing as exc:
                self.logger.warning(str(exc))
            if items:
                for item in items:
                    yield item
                break
        #Test - NOT WORKING - TypeError: 'ItemMeta' object does not support item assignment
        #ExtractedDataItem['PageURL'] = response.url

    def load_item(self, definition, response):
        query = response.xpath if definition.type == 'xpath' else response.css
        selectors = query(definition.selector)
        for selector in selectors:
            selector = selector if selector else None
            ld = PortiaItemLoader(
                item=definition.item(),
                selector=selector,
                response=response,
                baseurl=get_base_url(response)
            )
            for field in definition.fields:
                if hasattr(field, 'fields'):
                    if field.name is not None:
                        ld.add_value(field.name,
                                    self.load_item(field, selector))
                #H3: Save the page source URL
                elif field.name == 'PageURL':
                    ld.replace_value(field.name, response.url)
                elif field.type == 'xpath':
                    ld.add_xpath(field.name, field.selector, *field.processors,
                                 required=field.required)
                else:
                    ld.add_css(field.name, field.selector, *field.processors,
                               required=field.required)
                    #H3: If the field is PropDataList, break the list into individual fields of 
                    #PropDataCategory, PropAreaSize, PropDataBedroomsCount, PropDataBathroomsCount
                    if field.name == 'PropDataList':
                        valuePropDataList = response.xpath('//div[@class=\'highlight-title-value\']/text()').extract()
                        ld.replace_value('PropDataCategory', valuePropDataList[0])
                        ld.replace_value('PropAreaSize', valuePropDataList[1])
                        ld.replace_value('PropDataBedroomsCount', valuePropDataList[2])
                        ld.replace_value('PropDataBathroomsCount', valuePropDataList[3])
            yield ld.load_item()
