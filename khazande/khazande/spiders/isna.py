from datetime import datetime

import scrapy
import sqlalchemy as db


class IsnaSpider(scrapy.Spider):
    name = 'isna'
    allowed_domains = ['isna.ir']
    start_urls = ['https://www.isna.ir/page/archive.xhtml']

    def __init__(self):
        super().__init__()
        engine = db.create_engine(
            'postgresql://postgres:postgres@localhost/khabaryab')
        self.db_connection = engine.connect()
        metadata = db.MetaData()
        self.khabar_news = db.Table(
            'khabar_news', metadata, autoload=True, autoload_with=engine)
        khabar_news_agency = db.Table(
            'khabar_newsagency', metadata, autoload=True, autoload_with=engine)
        self.isna_id = self.db_connection.execute(db.select([khabar_news_agency]).where(
            khabar_news_agency.columns.name == "ایسنا")).fetchall()[0][0]

    def parse(self, response):
        news_list = response.css(".items > ul > li")
        for news in news_list:
            news_url = news.css("a::attr(href)").get()
            yield response.follow(news_url, callback=self.parse_news)

        next_page = response.css(".pagination > li")[-1]
        if "بعدی" not in next_page.get():
            return
        next_page_url = next_page.css("a::attr(href)").get()
        yield response.follow(next_page_url, callback=self.parse)

    def parse_news(self, response):
        title = response.css(".first-title::text").get()
        text = '\n'.join(response.css(".item-text > p::text").getall())
        url = response.url
        url = url[url.find("news/")+5:]
        news_id = url[:url.find("/")]
        published_at = datetime.now()
        if self.is_news_crawled_before(news_id) is False:
            self.db_connection.execute(db.insert(self.khabar_news).values(
                url=response.url, title=title, text=text, agency_id=self.isna_id, news_id=news_id, published_at=published_at
            ))

    def is_news_crawled_before(self, news_id):
        records = self.db_connection.execute(db.select([self.khabar_news]).where(
            self.khabar_news.columns.agency_id == self.isna_id,
            self.khabar_news.columns.news_id == news_id)).fetchall()
        if len(records) == 0:
            return False
        return True
