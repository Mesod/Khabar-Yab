import scrapy


class IsnaSpider(scrapy.Spider):
    name = 'isna'
    allowed_domains = ['isna.ir']
    start_urls = ['http://isna.ir/']

    def parse(self, response):
        pass
