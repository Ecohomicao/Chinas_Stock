# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from Stock.items import NameItem
from scrapy.selector import Selector
from scrapy.http import Request

class StockNameSpider(BaseSpider):
    name = "stock_name"
    #allowed_domains = ["http://app.finance.ifeng.com/list/"]
    start_urls = ["http://app.finance.ifeng.com/list/stock.php?t=ha&f=symbol&o=asc&p=1",
                  "http://app.finance.ifeng.com/list/stock.php?t=sa&f=symbol&o=asc&p=1"
    ]
    
    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//*[@class= "tab01"]/table/tr[position()>1]')
        for link in links:
            code = link.xpath('td[1]/a/text()').extract()
            name = link.xpath('td[2]/a/text()').extract()
            nameitem = NameItem()
            nameitem['code'] = code
            nameitem['name'] = name
            yield nameitem
        for url in sel.xpath('//*[@class= "tab01"]/table/tr[52]/td/a/@href').extract():
            url = "http://app.finance.ifeng.com/list/stock.php" + url
            yield Request(url, callback = self.parse)